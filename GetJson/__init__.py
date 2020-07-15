import logging
import json
import azure.functions as func
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('LOGGER: Python HTTP trigger function processed a request.')

    if req.method == 'POST':
        try:
            json_data = req.get_json()
            logging.info('LOGGER: preparing mail message. Raw json data: {}.'.format(json_data))
            api_key = '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'
            message_body = 'Hello Samo!<br><br>'
            message_body += 'This is your attached JSON:<br><br>'
            message_body += json.dumps(json_data) + '<br><br>'
            message_body += 'Regards<br>'
            message_body += 'your web hook tester'
            logging.info('LOGGER: mail message: {}.'.format(message_body))
            message = Mail(
                    from_email='noreply@nabla.si',
                    to_emails='samo.4tuna@gmail.com',
                    subject='Web Hook Tester - JSON data',
                    html_content=message_body)
            try:
                sg = SendGridAPIClient(api_key)
                response = sg.send(message)
                logging.info('LOGGER: sending mail successful. Response {}.'.format(response.status_code))
                return func.HttpResponse(
                    "All good",
                    status_code=200
                )
            except Exception as e:
                logging.info('LOGGER: sending mail failed. Reason {}.'.format(e))
                return func.HttpResponse(
                    "Sending mail failed",
                    status_code=500
                )
        except:
            return func.HttpResponse(
                "Bad Request - Not valid JSON",
                status_code=400
            )
    else:
        return func.HttpResponse(
                    "Service Unavailable",
                    status_code=503
                )
