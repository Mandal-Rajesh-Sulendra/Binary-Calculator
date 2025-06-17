
import streamlit as st

# Helper function to validate binary input
def is_binary(s):
    return all(char in '01' for char in s)

# Binary arithmetic operations
def binary_add(a, b):
    return bin(int(a, 2) + int(b, 2))[2:]

def binary_subtract(a, b):
    return bin(int(a, 2) - int(b, 2))[2:]

def binary_multiply(a, b):
    return bin(int(a, 2) * int(b, 2))[2:]

def binary_divide(a, b):
    if int(b, 2) == 0:
        raise ZeroDivisionError("Division by zero is not allowed.")
    return bin(int(a, 2) // int(b, 2))[2:]

# Streamlit UI
st.set_page_config(page_title="Binary Calculator", layout="centered")
st.title("🔢 Binary Arithmetic Calculator")

st.markdown("Enter two binary numbers and choose an operation.")

# Input fields
bin1 = st.text_input("Binary Number 1 (e.g. 1010)")
bin2 = st.text_input("Binary Number 2 (e.g. 0101)")
operation = st.selectbox("Select Operation", ["Addition", "Subtraction", "Multiplication", "Division"])

if st.button("Calculate"):
    # Validation
    if not is_binary(bin1) or not is_binary(bin2):
        st.error("Please enter valid binary numbers (only 0 and 1).")
    else:
        try:
            if operation == "Addition":
                result = binary_add(bin1, bin2)
            elif operation == "Subtraction":
                if int(bin1, 2) < int(bin2, 2):
                    st.error("Result would be negative. Not supported in binary unsigned mode.")
                    result = None
                else:
                    result = binary_subtract(bin1, bin2)
            elif operation == "Multiplication":
                result = binary_multiply(bin1, bin2)
            elif operation == "Division":
                result = binary_divide(bin1, bin2)

            if result is not None:
                st.success(f"✅ Binary Result: `{result}`")
                st.info(f"🧮 Decimal Result: `{int(result, 2)}`")
        except ZeroDivisionError as e:
            st.error(str(e))
