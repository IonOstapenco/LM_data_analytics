#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from typing import Any, Dict, List, Optional

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class FlexeraError(Exception):
    pass


class FlexeraClient:
    def __init__(
        self,
        graphql_url: str,
        refresh_token: str,
        zone: str = "eu",
        timeout: int = 30,
        verify_ssl: bool = False,
    ) -> None:
        self.graphql_url = graphql_url
        self.refresh_token = refresh_token
        self.zone = zone.lower().strip()
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        self.access_token: Optional[str] = None
        self.access_token_expiry: float = 0

        self.login_base = self._get_login_base()

        self.session = requests.Session()
        self.session.verify = self.verify_ssl

    def _get_login_base(self) -> str:
        mapping = {
            "com": "https://login.flexera.com",
            "eu": "https://login.flexera.eu",
            "au": "https://login.flexera.au",
        }
        if self.zone not in mapping:
            raise ValueError("zone deve essere una tra: com, eu, au")
        return mapping[self.zone]

    def _refresh_access_token(self) -> str:
        url = f"{self.login_base}/oidc/token"

        response = self.session.post(
            url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
            },
            timeout=self.timeout,
        )

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise FlexeraError(
                f"Errore durante il recupero del token: "
                f"HTTP {response.status_code} - {response.text}"
            ) from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise FlexeraError(
                f"Risposta non valida dall'endpoint token: {response.text}"
            ) from exc

        access_token = payload.get("access_token")
        expires_in = payload.get("expires_in", 3600)

        if not access_token:
            raise FlexeraError(
                "Risposta token non valida:\n"
                + json.dumps(payload, indent=2, ensure_ascii=False)
            )

        self.access_token = access_token
        self.access_token_expiry = time.time() + max(int(expires_in) - 60, 60)
        return access_token

    def _get_access_token(self) -> str:
        if not self.access_token or time.time() >= self.access_token_expiry:
            return self._refresh_access_token()
        return self.access_token

    def execute_graphql(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        operation_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        token = self._get_access_token()

        body: Dict[str, Any] = {
            "query": query,
            "variables": variables or {},
        }
        if operation_name:
            body["operationName"] = operation_name

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        response = self.session.post(
            self.graphql_url,
            headers=headers,
            json=body,
            timeout=self.timeout,
        )

        if response.status_code in (401, 403):
            token = self._refresh_access_token()
            headers["Authorization"] = f"Bearer {token}"

            response = self.session.post(
                self.graphql_url,
                headers=headers,
                json=body,
                timeout=self.timeout,
            )

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise FlexeraError(
                f"Errore HTTP sulla query GraphQL: "
                f"HTTP {response.status_code} - {response.text}"
            ) from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise FlexeraError(
                f"Risposta non valida dall'endpoint GraphQL: {response.text}"
            ) from exc

        if payload.get("errors"):
            raise FlexeraError(
                "GraphQL ha restituito errori:\n"
                + json.dumps(payload["errors"], indent=2, ensure_ascii=False)
            )

        return payload


def read_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def read_json_file(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("Il file JSON delle variables deve contenere un oggetto JSON")
    return data


def stringify_value(value: Any) -> str:
    if value is None:
        return ""

    if isinstance(value, (str, int, float, bool)):
        return str(value)

    if isinstance(value, list):
        if not value:
            return ""
        return " , ".join(stringify_value(item) for item in value)

    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False)

    return str(value)


def flatten_dict(
    data: Dict[str, Any],
    parent_key: str = "",
    sep: str = ".",
) -> Dict[str, str]:
    items: Dict[str, str] = {}

    for key, value in data.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key

        if isinstance(value, dict):
            items.update(flatten_dict(value, parent_key=new_key, sep=sep))

        elif isinstance(value, list):
            if not value:
                items[new_key] = ""

            elif all(isinstance(item, dict) for item in value):
                # Lista di oggetti con solo "name" -> stringa semplice
                if all(set(item.keys()) == {"name"} for item in value):
                    items[new_key] = " , ".join(
                        str(item.get("name", "")) for item in value
                    )

                # Lista con un solo oggetto -> espandi i campi
                elif len(value) == 1:
                    items.update(flatten_dict(value[0], parent_key=new_key, sep=sep))

                # Lista complessa -> JSON
                else:
                    items[new_key] = json.dumps(value, ensure_ascii=False)

            else:
                items[new_key] = stringify_value(value)

        else:
            items[new_key] = stringify_value(value)

    return items


def extract_first_list_from_data(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    for value in data.values():
        if isinstance(value, list) and all(isinstance(item, dict) for item in value):
            return value
        if isinstance(value, dict):
            nested = extract_first_list_from_data(value)
            if nested:
                return nested
    return []


def write_json(path: str, payload: Dict[str, Any], pretty: bool = True) -> None:
    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            payload,
            file,
            indent=2 if pretty else None,
            ensure_ascii=False,
        )


def write_csv(path: str, rows: List[Dict[str, Any]]) -> None:
    if not rows:
        raise ValueError("Nessuna riga trovata da esportare in CSV")

    flattened_rows = [flatten_dict(row) for row in rows]

    fieldnames: List[str] = []
    seen = set()

    for row in flattened_rows:
        for key in row.keys():
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)

    with open(path, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in flattened_rows:
            writer.writerow(row)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Esegue una query GraphQL su Flexera e salva il risultato in JSON/CSV."
    )

    parser.add_argument(
        "--graphql-url",
        required=True,
        help="URL completo dell'endpoint GraphQL Flexera",
    )
    parser.add_argument(
        "--query-file",
        required=True,
        help="Percorso del file .graphql/.qry/.txt contenente la query",
    )
    parser.add_argument(
        "--variables-file",
        help="Percorso del file JSON contenente le variables GraphQL",
    )
    parser.add_argument(
        "--operation-name",
        help="Nome operazione GraphQL opzionale",
    )
    parser.add_argument(
        "--refresh-token",
        default=os.getenv("FLEXERA_REFRESH_TOKEN"),
        help="Refresh token Flexera o variabile ambiente FLEXERA_REFRESH_TOKEN",
    )
    parser.add_argument(
        "--zone",
        default=os.getenv("FLEXERA_ZONE", "eu"),
        help="Zona Flexera: com, eu, au",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Timeout HTTP in secondi",
    )
    parser.add_argument(
        "--verify-ssl",
        action="store_true",
        help="Abilita la verifica SSL (default: disabilitata)",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Stampa il JSON formattato a video",
    )
    parser.add_argument(
        "--output-json",
        help="Salva la risposta completa in un file JSON",
    )
    parser.add_argument(
        "--output-csv",
        help="Salva il primo array trovato nella response GraphQL in CSV",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not args.refresh_token:
        print(
            "Errore: manca --refresh-token o FLEXERA_REFRESH_TOKEN",
            file=sys.stderr,
        )
        return 1

    try:
        query = read_text_file(args.query_file)
        variables = read_json_file(args.variables_file) if args.variables_file else {}

        client = FlexeraClient(
            graphql_url=args.graphql_url,
            refresh_token=args.refresh_token,
            zone=args.zone,
            timeout=args.timeout,
            verify_ssl=args.verify_ssl,
        )

        result = client.execute_graphql(
            query=query,
            variables=variables,
            operation_name=args.operation_name,
        )

        if args.pretty:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(json.dumps(result, ensure_ascii=False))

        if args.output_json:
            write_json(args.output_json, result, pretty=True)

        if args.output_csv:
            rows = extract_first_list_from_data(result.get("data", {}))
            write_csv(args.output_csv, rows)

        return 0

    except Exception as exc:
        print(f"Errore: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())