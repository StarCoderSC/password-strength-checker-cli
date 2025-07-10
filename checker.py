
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich import print as rprint
import sys
import re
import os
import argparse
import csv
from datetime import datetime

console = Console()

def check_password_strength(password):
    strength = 0
    remarks = []

    if len(password) >= 8:
        strength += 1
    else:
        remarks.append("Too short")
    
    if re.search(r'[A-Z]', password):
        strength += 1
    else:
        remarks.append("Missing uppercase")
    
    if re.search(r'[a-z]', password):
        strength += 1
    else:
        remarks.append("Missing lowercase")
    
    if re.search(r'\d', password):
        strength += 1
    else:
        remarks.append("Missing number")
    
    if re.search(r'[!@#$%^&*()_+?/\,."{}|<>]', password):
        strength += 1
    else:
        remarks.append("Missing special char")
    
    return strength, remarks

def bulk_check(filename="password.txt", output_path=None):
    if not os.path.exists(filename):
        console.print(f"[red]File '{filename}' not found!")
        return
        
    
    console.print(f"[bold blue] Checking passwords from: [underline]{filename}")
    table = Table(title="Bulk password Strength Report", show_lines=True)

    table.add_column("Password", style="cyan", overflow="fold")
    table.add_column("Score", style="bold green")
    table.add_column("Remarks", style="yellow")



    if output_path:
        if not output_path.lower().endswith('.csv'):
            output_path += '.csv'

        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(os.path.dirname(output_dir), exist_ok=True)

        if os.path.exists(output_path):
            confirm = Prompt.ask(f"[yellow bold]'{output_path}' already exists. Overwrite? (y/n):[/]")
            if confirm.strip().lower() != "y":
                console.print("[bold red] Export cancelled by user.")
                return
        output_csv = output_path

    else:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_csv = f"password_report_{timestamp}.csv"
            
    csv_rows = [("Password", "Score", "Remarks")]

    with open(filename, 'r') as file:
        for line in file:
            password = line.strip()
            if not password:
                continue
            strength, remarks = check_password_strength(password)
            score_str = f"{strength}/5"

            if strength == 5:
                remarks_text = "Strong"
                display_remarks = "[green]Strong"

            elif strength >= 3:
                remarks_text = "Moderate: " + ", ".join(remarks)
                display_remarks = "[yellow]" + remarks_text

            else:
                remarks_text = "Weak: " + ", ".join(remarks)
                display_remarks = "[red]" + remarks_text
            
            table.add_row(password, score_str, display_remarks)
            csv_rows.append(((password, score_str, remarks_text)))

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_rows)
     
    console.print(table)
    console.print(f"\n[bold green]Report saved to:[/][underline]{output_csv}[/]")

def single_check():
    pwd = Prompt.ask("Enter Password", password=True)
    confirm = Prompt.ask("Confirm password", password=True)
    if pwd != confirm:
        console.print("[red] Passwords don't match.")
    else:
        score, remarks = check_password_strength(pwd)
        console.print(f"[bold]Score:[/]{score}/5")
        if remarks:
            for r in remarks:
                console.print(f" -[red]{r}")
        else:
            console.print("[green]Strong password!")


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Password Strength Checker CLI")
    parser.add_argument('--file', help="Bulk check passwords from a .txt file")
    parser.add_argument("--output", help="Optional: Export CSV to custom path (only with --file)")
    args = parser.parse_args()

    console.rule("[bold magenta]🔐 Password Strength Checker")
    console.print("[bold green]CLI Tool to check password strength via rules: length, cases, numbers, special characters.[/]")

    if args.file:
        bulk_check(args.file, output_path=args.output)
    else:
        console.print("[bold blue]No file provided.[/]")
        console.print("[bold green]Choose an option:[/]")
        console.print("1. [cyan]Single Password[/]")
        console.print("2. [cyan]Bulk Check from default 'passwords.txt'[/]")
        choice = Prompt.ask("Enter 1 or 2").strip()

        if choice == "1":
            single_check()
        elif choice == "2":
            bulk_check("password.txt")
        else:
            rprint("[red]Invalid choice....[/]")
            sys.exit()
