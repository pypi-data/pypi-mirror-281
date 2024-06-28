from dotenv import load_dotenv
import os
from sync_mailchimp_entra.core import sync
from sync_mailchimp_entra.core.mailchimp import MailchimpClient
from sync_mailchimp_entra.core.graph import GraphClient


async def main():
    load_dotenv(override=True)

    # Config Graph
    GraphClient.get_instance(
        os.getenv("TENANT_ID"),
        os.getenv("APPLICATION_ID"),
        os.getenv("APPLICATION_SECRET"),
        ["https://graph.microsoft.com/.default"],
    )
    entra_group_id = os.getenv("ENTRA_GROUP_ID")

    # Config Mailchimp
    for i in range(1, int(os.getenv("NB_MAILCHIMP")) + 1):
        print(f"\nBeginning sync for Mailchimp {i}.")
        MailchimpClient.get_instance(
            os.getenv("API_TOKEN_MAILCHIMP" + str(i)),
            os.getenv("SERVER_PREFIX" + str(i)),
        )
        list_mailchimp_id = os.getenv("LIST_MAILCHIMP_ID" + str(i))

        await sync.mailchimp_entra(list_mailchimp_id, entra_group_id)
        print(f"Sync for Mailchimp {i} finished.")
