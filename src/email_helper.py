import os
import smtplib

import logging
import pandas as pd
from typing import List
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SENDER_EMAIL = "xuyan.nus@gmail.com"
RECEIVER_EMAILS = ["xuyan.nus@gmail.com", "hongyu.ju@gmail.com"]


def email_bid_prices(alerts: pd.DataFrame, to_recipient_columns: List):
    logging.info("str(len(alerts)):" + str(len(alerts)))

    if len(alerts) > 0:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = ','.join(RECEIVER_EMAILS)
        msg['Subject'] = "Stock Price Shake 5%+ Notice"

        # to avoid to_html() truncates long URL
        pd.set_option('display.max_colwidth', -1)

        msg.attach(MIMEText(alerts.to_html(index=False, columns=to_recipient_columns, float_format='{:,.3f}'.format), 'html'))

        for a_plot_path in alerts['plot'].values:
            if a_plot_path is None:
                continue

            with open(a_plot_path, "rb") as a_plot_reader:
                photo_attachment = MIMEBase('application', "octet-stream")
                photo_attachment.set_payload(a_plot_reader.read())

            encoders.encode_base64(photo_attachment)
            photo_attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(a_plot_path))
            msg.attach(photo_attachment)

        with smtplib.SMTP('localhost') as email_server:
            email_server.sendmail(SENDER_EMAIL, RECEIVER_EMAILS, msg.as_string())
