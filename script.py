import pandas as pd
from bs4 import BeautifulSoup

# Load and parse HTML
with open('unclaimed_property_sample.html', 'r') as f:
    soup = BeautifulSoup(f, 'html.parser')

table = soup.find('table')
headers = [th.text.strip() for th in table.find_all('th')]

rows = []
for tr in table.find('tbody').find_all('tr'):
    rows.append([td.text.strip() for td in tr.find_all('td')])

df = pd.DataFrame(rows, columns=headers)

# Clean Owner Name
def clean_name(name):
    last, first = [x.strip() for x in name.split(',', 1)]
    tokens = first.title().split()
    tokens = [t + '.' if len(t) == 1 else t for t in tokens]
    return " ".join(tokens + [last.title()])

df['Owner Name'] = df['Owner Name'].apply(clean_name)

# Convert Amount to float
df['Amount'] = (
    df['Amount']
    .replace({r'[\$,]': ''}, regex=True)
    .astype(float)
)

# Claim Score
def claim_score(amount):
    if amount > 500:
        return 10
    elif amount >= 100:
        return 7
    return 3

df['Claim Score'] = df['Amount'].apply(claim_score)

# Dummy Email
def make_email(name):
    parts = name.split()
    last = parts[-1].lower()
    firsts = [p.lower().rstrip('.') for p in parts[:-1]]
    return ".".join(firsts + [last]) + "@email.com"

df['Email'] = df['Owner Name'].apply(make_email)

if __name__ == "__main__":
    print(df)
