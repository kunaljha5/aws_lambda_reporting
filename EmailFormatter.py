import boto3, logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('Loading function')

#CONFIGURATION_SET = "ConfigSet"
RECIPIENT = "kunaljha5@gmail.com"
SENDER = "Kunal Jha <kunaljha5@gmail.com>"
AWS_REGION = "us-east-1"
SUBJECT = "Amazon SES Test (SDK for Python)"
client = boto3.client('ses', region_name=AWS_REGION)
CHARSET = "UTF-8"
logger.info(SUBJECT)
ssm = boto3.client('ssm')


def master_function() :
    parameter = ssm.get_parameter(Name='/Sonar/Report/Details/BaseUrl', WithDecryption=True)
    base_url = (parameter['Parameter']['Value'])
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                 "This email was sent with Amazon SES using the "
                 "AWS SDK for Python (Boto)."
                 )
    BODY_TEXT = BODY_TEXT + "\n" + base_url

    # The HTML body of the email.

    BODY_HTML = """<!DOCTYPE html>
        <html lang="en">
        <head>
        <title>Sonar Report</title>
        <style>
        th, td {
        border: 1px solid  black;
        text-align: center;
        height: 1px;
        vertical-align: bottom;
        padding: 5px;
        font-family: courier;
        font-size: 75%
        }
        table {
          font-family: courier;
           background-color: white;
        }
        tr:hover {background-color: #f5f5f5;}
        tr:nth-child(even) {background-color: #f2f2f2;}
        </style>
        </head>
        <body><table float=left border=1px width='99%' align=center>
        <tr>
        <th colspan=8 bgcolor=#66ff00 text-align=center >SONAR STATUS</th>
        </tr>
        <tr>
        <th bgcolor=#66ff00 text-align=center>Project_Name</th>
        <th bgcolor=#66ff00 text-align=center>Bugs</th>
        <th bgcolor=#66ff00 text-align=center>Code_Smells</th>
        <th bgcolor=#66ff00 text-align=center>Code_Coverage</th>
        <th bgcolor=#66ff00 text-align=center>Vulnerabilities</th>
        <th bgcolor=#66ff00 text-align=center>Last_Analysis_Date</th>
        </tr>
        <tr>
        <td><a href='http://test-sonar-build.dummy.net:9000/dashboard?id=com.dummy:app1'>app1</a></td>
        <td>100</td>
        <td>811</td>
        <td bgcolor=Fuchsia>0.0</td>
        <td>108</td>
        <td>2019-05-12</td></tr>
        <td><a href='http://test-sonar-build.dummy.net:9000/dashboard?id=com.dummy:app2'>app2</a></td>
        <td>0</td>
        <td>5</td>
        <td>93.5</td>
        <td>0</td>
        <td>2019-11-08</td></tr>

        </table><br>
        </br>
        </body>
        <p>Sender : Admin</p>
    </html>"""

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER
            # If you are not using a configuration set, comment or delete the
            # following line
            #ConfigurationSetName=CONFIGURATION_SET
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


logger.info(CHARSET)
if __name__ == '__main__':
    # test1.py executed as script
    # do something
    master_function()
