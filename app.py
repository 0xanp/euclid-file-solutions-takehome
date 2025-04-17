import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup

st.set_page_config(page_title="Euclid File Solutions Takehome Assignment", layout="wide")
st.title("🗂️ Euclid File Solutions Takehome Assignment")
st.markdown("Upload your HTML file in the original unclaimed property format and watch it transform step by step.")

uploaded_file = st.file_uploader("Upload HTML file", type=["html"], help="Select the HTML file exported from your unclaimed property system.")

if uploaded_file:
    # Step 1: Raw Data Extraction
    html_content = uploaded_file.read().decode("utf-8")
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')
    headers = [th.text.strip() for th in table.find_all('th')]
    raw_rows = []
    for tr in table.find('tbody').find_all('tr'):
        raw_rows.append([td.text.strip() for td in tr.find_all('td')])
    raw_df = pd.DataFrame(raw_rows, columns=headers)

    st.subheader("1️⃣ Raw Data Preview")
    st.code(
        '''# Read and parse HTML
html_content = uploaded_file.read().decode("utf-8")
soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find('table')
headers = [th.text.strip() for th in table.find_all('th')]
raw_rows = []
for tr in table.find('tbody').find_all('tr'):
    raw_rows.append([td.text.strip() for td in tr.find_all('td')])
raw_df = pd.DataFrame(raw_rows, columns=headers)''',
        language='python'
    )
    st.dataframe(raw_df)

    # Step 2: Normalize Owner Name
    def clean_name(name):
        last, first = [x.strip() for x in name.split(',', 1)]
        tokens = first.title().split()
        tokens = [t + '.' if len(t) == 1 else t for t in tokens]
        return " ".join(tokens + [last.title()])

    df = raw_df.copy()
    df['Owner Name'] = df['Owner Name'].apply(clean_name)

    st.subheader("2️⃣ Normalized Owner Names")
    st.code(
        '''def clean_name(name):
    last, first = [x.strip() for x in name.split(',', 1)]
    tokens = first.title().split()
    tokens = [t + '.' if len(t) == 1 else t for t in tokens]
    return " ".join(tokens + [last.title()])

df = raw_df.copy()
df['Owner Name'] = df['Owner Name'].apply(clean_name)''',
        language='python'
    )
    st.dataframe(df[['Owner Name']])

    # Step 3: Convert Amount to Float
    df['Amount'] = df['Amount'].replace({r'[\$,]': ''}, regex=True).astype(float)
    st.subheader("3️⃣ Amount as Float")
    st.code(
        '''# Convert Amount field
df['Amount'] = df['Amount'].replace({r'[\$,]': ''}, regex=True).astype(float)''',
        language='python'
    )
    st.dataframe(df[['Amount']])

    # Step 4: Add Claim Score
    def claim_score(amount):
        if amount > 500:
            return 10
        elif amount >= 100:
            return 7
        return 3
    df['Claim Score'] = df['Amount'].apply(claim_score)

    st.subheader("4️⃣ Claim Score Assigned")
    st.code(
        '''def claim_score(amount):
    if amount > 500:
        return 10
    elif amount >= 100:
        return 7
    return 3

df['Claim Score'] = df['Amount'].apply(claim_score)''',
        language='python'
    )
    st.dataframe(df[['Amount', 'Claim Score']])

    # Step 5: Dummy Email Enrichment
    def make_email(name):
        parts = name.split()
        last = parts[-1].lower()
        firsts = [p.lower().rstrip('.') for p in parts[:-1]]
        return ".".join(firsts + [last]) + "@email.com"
    df['Email'] = df['Owner Name'].apply(make_email)

    st.subheader("5️⃣ Email Enrichment (Dummy)")
    st.code(
        '''def make_email(name):
    parts = name.split()
    last = parts[-1].lower()
    firsts = [p.lower().rstrip('.') for p in parts[:-1]]
    return ".".join(firsts + [last]) + "@ email.com"

df['Email'] = df['Owner Name'].apply(make_email)''',
        language='python'
    )
    st.dataframe(df[['Owner Name', 'Email']])

    # Final Processed Data with Code Expander
    st.subheader("✅ Final Processed Data")
    st.dataframe(df)
    
    full_script = '''
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup

st.set_page_config(page_title="Unclaimed Property Processor", layout="wide")
st.title("🗂️ Unclaimed Property Data Processor")
st.markdown("Upload your HTML file in the original unclaimed property format and watch it transform step by step.")

uploaded_file = st.file_uploader("Upload HTML file", type=["html"], help="Select the HTML file exported from your unclaimed property system.")

if uploaded_file:
    html_content = uploaded_file.read().decode("utf-8")
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')
    headers = [th.text.strip() for th in table.find_all('th')]
    raw_rows = []
    for tr in table.find('tbody').find_all('tr'):
        raw_rows.append([td.text.strip() for td in tr.find_all('td')])
    raw_df = pd.DataFrame(raw_rows, columns=headers)
    df = raw_df.copy()
    df['Owner Name'] = df['Owner Name'].apply(clean_name)
    df['Amount'] = df['Amount'].replace({r'[\\$,]': ''}, regex=True).astype(float)
    df['Claim Score'] = df['Amount'].apply(claim_score)
    df['Email'] = df['Owner Name'].apply(make_email)
    st.dataframe(df)
'''    
    with st.expander("🔍 Show Full Script"):
        st.code(full_script, language='python')
else:
    st.info("Please upload an HTML file to begin processing.")
