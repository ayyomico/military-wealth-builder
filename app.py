
import streamlit as st

# Set up page configuration
st.set_page_config(
    page_title="Military Wealth Builder",
    page_icon="🏛️",
    layout="centered"
)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Pay chart (example)
pay_chart = {
    'E-4': {'Under 2': 2664, 'Over 2': 2829, 'Over 3': 2829, 'Over 4': 2829},
    'E-5': {'Under 2': 2904, 'Over 2': 3101, 'Over 3': 3195, 'Over 4': 3234},
    'E-6': {'Under 2': 3174, 'Over 2': 3418, 'Over 3': 3515, 'Over 4': 3612},
}

# Allowances
BAS_AMOUNT = 452.56
DEFAULT_BAH = 1800

# Home Page
if st.session_state.page == 'home':
    st.title("🏛️ Military Wealth Builder")
    st.markdown("Welcome, Warrior! Let's build your financial battle plan.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start Budget Setup ➡️"):
            st.session_state.page = 'budget_setup'
    with col2:
        if st.button("Input Debts ➡️"):
            st.session_state.page = 'input_debts'

# Budget Setup
if st.session_state.page == 'budget_setup':
    st.title("💰 Income Setup")
    rank = st.selectbox("Select your Rank", list(pay_chart.keys()))
    yos = st.selectbox("Select your Years of Service", list(pay_chart[rank].keys()))
    base_pay = pay_chart[rank][yos]
    bah = st.number_input("Enter your BAH (Monthly)", value=DEFAULT_BAH)
    bas = st.number_input("Enter your BAS (Monthly)", value=BAS_AMOUNT)
    other_income = st.number_input("Other Special Pays (Monthly)", value=0.0)
    total_income = base_pay + bah + bas + other_income
    st.session_state.total_income = total_income
    st.metric("Total Monthly Income", f"${total_income:,.2f}")
    if st.button("Next ➡️"):
        st.session_state.page = 'input_debts'

# Debts Page
if st.session_state.page == 'input_debts':
    st.title("💳 Input Your Debts")
    if 'debts' not in st.session_state:
        st.session_state.debts = []
    with st.form(key='debt_form', clear_on_submit=True):
        name = st.text_input("Debt Name")
        balance = st.number_input("Balance Remaining ($)", min_value=0.0)
        rate = st.number_input("Interest Rate (%)", min_value=0.0)
        min_pay = st.number_input("Minimum Monthly Payment ($)", min_value=0.0)
        if st.form_submit_button("Add Debt"):
            st.session_state.debts.append({"Debt Name": name, "Balance": balance, "Rate": rate, "Min Payment": min_pay})
    if st.session_state.debts:
        st.write(st.session_state.debts)
    if st.button("Save and Continue ➡️"):
        st.session_state.page = 'expenses_setup'

# Expenses Page
if st.session_state.page == 'expenses_setup':
    st.title("💸 Expenses Setup")
    if 'expenses' not in st.session_state:
        st.session_state.expenses = []
    with st.form(key='expenses_form', clear_on_submit=True):
        name = st.text_input("Expense Name")
        amount = st.number_input("Monthly Cost ($)", min_value=0.0)
        if st.form_submit_button("Add Expense"):
            st.session_state.expenses.append({"Expense Name": name, "Amount": amount})
    if st.session_state.expenses:
        st.write(st.session_state.expenses)
    if st.button("Save and Continue ➡️"):
        st.session_state.page = 'budget_overview'

# Budget Overview Page
if st.session_state.page == 'budget_overview':
    st.title("📊 Budget Overview")
    income = st.session_state.total_income
    expenses = sum(x['Amount'] for x in st.session_state.expenses)
    min_payments = sum(x['Min Payment'] for x in st.session_state.debts)
    free_cash = income - (expenses + min_payments)
    st.session_state.free_cash = free_cash
    st.metric("Free Cash Flow", f"${free_cash:,.2f}")
    st.progress(min(1, free_cash / income))
    if st.button("Start My Action Plan ➡️"):
        st.session_state.page = 'action_plan'

# Action Plan
if st.session_state.page == 'action_plan':
    st.title("🗂️ Action Plan")
    free_cash = st.session_state.free_cash
    debt_split = st.slider("% Toward Debt Payoff", 0, 100, 70)
    savings_split = 100 - debt_split
    debt_amount = (debt_split / 100) * free_cash
    savings_amount = (savings_split / 100) * free_cash
    st.metric("Debt Allocation", f"${debt_amount:,.2f}")
    st.metric("Savings Allocation", f"${savings_amount:,.2f}")
    if st.button("Confirm Plan ➡️"):
        st.session_state.page = 'confirmation'

# Final Confirmation
if st.session_state.page == 'confirmation':
    st.title("🏆 Mission Accepted!")
    st.markdown("Congratulations, Warrior! You've created your plan to destroy debt and build wealth.")
    st.write(f"**Debt Focus:** {st.session_state.debts[0]['Debt Name']}" if st.session_state.debts else "No debts entered.")
    st.write(f"Estimated months to debt-free: ~12 months (simple est.)")
    st.success("Discipline equals freedom. 
- Jocko Willink")
    if st.button("Return Home"):
        st.session_state.page = 'home'
