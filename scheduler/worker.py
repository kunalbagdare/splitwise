import requests
import jinja2
import settings
import requests
from models import PassbookModel, UserModel

domain = settings.MAILGUN_DOMAIN
key = settings.MAILGUN_API_KEY

def send_email_by_mailgun(html,to_email,subject):
    """
    The function `send_email_by_mailgun` sends an email using the Mailgun API, with the specified HTML
    content, recipient email address, and subject.
    
    """
        
    request_url = f"https://api.mailgun.net/v3/{domain}/messages"
    response = requests.post(
        request_url,
        auth=("api", key),
        data={
            "from": "service@splitwise.com", 
            "to": to_email,
            "html":html,
            "subject": subject,
        },
    )

def create_and_send_weekly_emails():
    """
    The function `create_and_send_weekly_emails` retrieves payee entries from a database, calculates the
    total amount for each payer, creates a weekly summary template, and sends an email to the payee with
    the summary using the Mailgun service.
    """

    users = UserModel.query.all()
    for user in users:
        payee_entries = PassbookModel.query.filter_by(payee_id=user.id).all()
        if not len(payee_entries):
            return None
        
        final_data_for_user = {}
        payee_name = payee_entries[0].payee.name
        payee_email = payee_entries[0].payee.email

        for entry in payee_entries:
            payer_name = entry.payer.name
            if payer_name not in final_data_for_user:
                final_data_for_user[payer_name] = entry.amount
            else:
                final_data_for_user[payer_name] += entry.amount

    html = create_weekly_template(payee_name,final_data_for_user)
    subject = "Weekly Summary Splitwise"
    send_email_by_mailgun(html,payee_email,subject)

        
def send_email_on_expense(expense_id):
    """
    The function sends an email notification to the payee about an expense they owe to the payer.
    """

    passbook_entry = PassbookModel.query.filter_by(expense_id=expense_id).all()

    for data in passbook_entry:
        payer_name = data.payer.name
        payee_name = data.payee.name
        amount_owed = data.amount
        expense_name = data.expense.expense_name
        to_email = data.payee.email
        if payer_name == payee_name:
            continue

        html = create_expense_template(payer_name,payee_name,amount_owed,expense_name)
        subject = "Expense Notification"
        send_email_by_mailgun(html,to_email,subject)

def create_expense_template(payer_name,payee_name,amount_owed,expense_name):
    """
    The function `create_template` uses a Jinja2 template to render an HTML file with the provided values
    and return rendered template with the provided variables.
    """

    templateLoader = jinja2.FileSystemLoader(searchpath='./scheduler/')
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "expense_template.html"
    template = templateEnv.get_template(TEMPLATE_FILE)
    outputText = template.render(payer_name=payer_name,payee_name=payee_name,
                                 amount_owed=amount_owed,expense_name=expense_name)
    
    return outputText


def create_weekly_template(payee_name,output_data):
    """
    The function `create_weekly_template` takes in a payee name and output data, and uses a Jinja2
    template to generate a weekly template HTML file with the provided data.

    """

    templateLoader = jinja2.FileSystemLoader(searchpath='./scheduler/')
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "weekly_template.html"
    template = templateEnv.get_template(TEMPLATE_FILE)
    outputText = template.render(payee_name=payee_name,
                                output=output_data)
    
    return outputText