# from frappeclient import FrappeClient
#
#
# @frappe.whitelist(allow_guest=True)
# def fetch_teller():
#     conn = FrappeClient("https://erpnext15.prod:620",verify=False)
#     conn.login("administrator", "123456",)
#     # Connect to the frappe-prod instance
#     # client = FrappeClient("https://erpnext15.prod:620", "administrator", "123456")
#
#     # # Fetch all Teller Invoices
#     invoices = conn.get_list("Teller Invoice", fields=["*"])
#
#     # # Insert all invoices into frappe-dev
#     for invoice in invoices:
#         return invoice
#
#     #     return invoice
#     #     doc = frappe.get_doc({
#     #         'doctype': 'Teller Invoice',
#     #         # Add all the necessary fields here
#     #     })
#     #     doc.insert()
#
#     # frappe.db.commit()

from frappeclient import FrappeClient
import frappe


@frappe.whitelist(allow_guest=True)
def get_sales_invoice():
    try:
        # Initialize FrappeClient for production instance and disable SSL verification
        conn_prod = FrappeClient("http://127.0.0.1:620", verify=False)
        # Login to the Frappe production instance
        session_prod = conn_prod.login("administrator", "123456")

        # Check if logged in successfully
        if not session_prod:
            return "Error: Could not log in to the production instance."

        # Fetch Teller Invoices from production instance
        invoices_prod = conn_prod.get_list("Teller Invoice")
        # print(invoices_prod)

        # Initialize FrappeClient for development instance and disable SSL verification
        conn_dev = FrappeClient("http://127.0.0.1:8001", verify=False)
        # Login to the Frappe development instance
        session_dev = conn_dev.login("administrator", "123456")

        # Check if logged in successfully
        if not session_dev:
            return "Error: Could not log in to the development instance."

        return invoices_prod



    except Exception as e:
        # Handle any errors that may occur during the process
        error_msg = f"Error fetching or inserting Teller Invoices: {str(e)}"
        frappe.log_error(error_msg)
        return error_msg


@frappe.whitelist(allow_guest=True)
def fetch_and_insert_item():
    try:
        # Initialize FrappeClient for development instance and disable SSL verification
        conn_dev = FrappeClient("http://127.0.0.1:8001", verify=False)
        # Login to the Frappe development instance
        session_dev = conn_dev.login("administrator", "123456")

        # Check if logged in successfully
        if not session_dev:
            return "Error: Could not log in to the development instance."

        # Fetch Item Price List from development instance
        item_list_dev = conn_dev.get_list("Item")

        # Initialize FrappeClient for production instance and disable SSL verification
        conn_prod = FrappeClient("http://127.0.0.1:620", verify=False)
        # Login to the Frappe production instance
        session_prod = conn_prod.login("administrator", "123456")

        # Check if logged in successfully
        if not session_prod:
            return "Error: Could not log in to the production instance."

        # Insert Item Price List into production instance
        # for item_price in item_list_dev:
        #     conn_prod.insert(item_price)

        # return "Item Price List inserted successfully."
        teller = conn_prod.insert({
            "doctype": "Teller Invoice",
            "client_type": 'Individual',
            "movement_number": 77

        })
        return teller

    except Exception as e:
        # Handle any errors that may occur during the process
        error_msg = f"Error fetching or inserting Item Price List: {str(e)}"
        frappe.log_error(error_msg)
        return error_msg

#update the
@frappe.whitelist(allow_guest=True)
def update_item_price():
    rate_list=[]
    try:
        # Initialize FrappeClient for development instance and disable SSL verification
        conn_dev = FrappeClient("http://127.0.0.1:8001", verify=False)
        # Login to the Frappé development instance
        session_dev = conn_dev.login("administrator", "123456")

        # Check if logged in successfully
        if not session_dev:
            return "Error: Could not log in to the development instance."

        # Fetch Item Price List from development instance
        item_list_dev = conn_dev.get_list("Item Price")

        # Initialize FrappeClient for production instance and disable SSL verification
        conn_prod = FrappeClient("http://127.0.0.1:620", verify=False)
        # Login to the Frappé production instance
        session_prod = conn_prod.login("administrator", "123456")

        # Check if logged in successfully
        if not session_prod:
            return "Error: Could not log in to the production instance."

        # Fetch Item Price List from development instance and update them in production instance
        for item in item_list_dev:
            price_list_rate = conn_dev.get_value("Item Price", "price_list_rate", {"item_code": item["item_code"]})['price_list_rate']
            rate_list.append(price_list_rate)
        # return price_list_rate
            custom_selling_rate = conn_dev.get_value("Item Price", "custom_selling_rate", {"item_code": item["item_code"]})['custom_selling_rate']
            rate_list.append(custom_selling_rate)
            custom_selling_special_rate = conn_dev.get_value("Item Price", "custom_selling_special_rate", {"item_code": item["item_code"]})['custom_selling_special_rate']
            rate_list.append(custom_selling_special_rate)
            custom_purchase_special_rate = conn_dev.get_value("Item Price", "custom_purchase_special_rate", {"item_code": item["item_code"]})['custom_purchase_special_rate']
            rate_list.append(custom_purchase_special_rate)
        # return rate_list

            #Update the item prices in the production instance
            conn_prod.set_value("Item Price", item["name"], "price_list_rate", price_list_rate)
            conn_prod.set_value("Item Price", item["name"], "custom_selling_rate", custom_selling_rate)
            conn_prod.set_value("Item Price", item["name"], "custom_selling_special_rate", custom_selling_special_rate)
            conn_prod.set_value("Item Price", item["name"], "custom_purchase_special_rate", custom_purchase_special_rate)
        #
        # return "Item prices updated successfully in the production instance."
        # return item_list_dev

    except Exception as e:
        # Handle any errors that may occur during the process
        error_msg = f"Error fetching or updating Item Price List: {str(e)}"
        frappe.log_error(error_msg)
        return error_msg

