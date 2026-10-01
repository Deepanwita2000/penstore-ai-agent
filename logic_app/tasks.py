from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def send_email_task(
    self,
    to_email,
    subject,
    body,
    image_urls=None,
):

    image_urls = image_urls or []

    html_body = f"""
    <html>
        <body>
            <p>{body.replace(chr(10), "<br>")}</p>
    """

    if image_urls:

        html_body += """
        <h3>Product Images</h3>
        """

        for image_url in image_urls:

            html_body += f"""
            <div>
                <img
                    src="{image_url}"
                    style="max-width:500px;"
                >
                <br>
                <a href="{image_url}">
                    View Image
                </a>
            </div>
            <br>
            """

    html_body += """
        </body>
    </html>
    """
    print(html_body)
    email = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )

    email.attach_alternative(
        html_body,
        "text/html"
    )
    print(html_body)

    email.send()

    return {
        "success": True,
        "message": "Email sent successfully.",
        "to_email": to_email,
    }