from celery import shared_task
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

@shared_task
def generate_crm_report():
    try:
        # Set up GraphQL client
        transport = RequestsHTTPTransport(
            url='http://localhost:8000/graphql', 
            verify=True, 
            retries=3
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        
        # GraphQL query to fetch CRM data
        query = gql('''
        query {
            customers {
                id
            }
            orders {
                id
                totalAmount
            }
        }
        ''')
        
        # Execute the query
        response = client.execute(query)
        
        # Extract data
        customers = response.get('customers', [])
        orders = response.get('orders', [])
        
        num_customers = len(customers)
        total_orders = len(orders)
        total_revenue = sum(float(order.get('totalAmount', order.get('total_amount', 0))) for order in orders)
        
        # Log the report
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        report_line = f"{timestamp} - Report: {num_customers} customers, {total_orders} orders, {total_revenue:.2f} revenue\n"
        
        with open("/tmp/crm_report_log.txt", "a") as f:
            f.write(report_line)
            
        return f"Report generated successfully: {num_customers} customers, {total_orders} orders, {total_revenue:.2f} revenue"
        
    except Exception as e:
        error_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        error_line = f"{error_timestamp} - Error generating report: {str(e)}\n"
        
        with open("/tmp/crm_report_log.txt", "a") as f:
            f.write(error_line)
            
        return f"Error generating report: {str(e)}"
