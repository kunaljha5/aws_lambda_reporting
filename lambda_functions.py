import logging
import EmailFormatter

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('Loading function')


def lambda_handler(event, context):
    logger.info(event)
    #print(event)
    #print(context)
    output = {'purpose': 'Hello World'}
    print("BeforeEmail")
    out  =  EmailFormatter.master_function()
    print("AfterEmail")
    print(out)
    return output


lambda_handler("kunal", "jha")
