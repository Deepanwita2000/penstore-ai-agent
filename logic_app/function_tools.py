from logic_app.models import PenProduct
from logic_app.tasks import send_email_task


def get_all_products():
    products = (
        PenProduct.objects
        .all()
        .values(
            "id",
            "name",
            "price",
            "scheme",
            "quantity_condition"
        )
    )

    products = list(products)

    if not products:
        return {
            "success": False,
            "message": "No products are currently available."
        }

    return {
        "success": True,
        "products": products
    }


def get_product_info(product_name: str):

    product = (
        PenProduct.objects
        .filter(name__icontains=product_name)
        .prefetch_related("images")
        .first()
    )

    if not product:
        return {
            "success": False,
            "message": "Product not found. Ask the customer to clarify the product name."
        }

    images = [
        image.image.url
        for image in product.images.all()
        if image.image
    ]

    return {
        "success": True,
        "product": {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "scheme": product.scheme,
            "quantity_condition": product.quantity_condition,
            "images": images,
        }
    }


def get_top_ten_products():

    products = (
        PenProduct.objects
        .all()
        .values(
            "id",
            "name",
            "price",
            "scheme",
            "quantity_condition"
        )   [:10]
    )
    print(products)

    return {
        "success": True,
        "products": list(products)
    }


def get_products_by_range(start: int, end: int):
    try:
        start = int(start)
        end = int(end)
    except (TypeError, ValueError):
        return {
            "success": False,
            "message": "Start and end prices must be valid numbers."
        }

    if start < 0 or end < 0:
        return {
            "success": False,
            "message": "Price cannot be negative."
        }

    if start > end:
        return {
            "success": False,
            "message": "Minimum price cannot be greater than maximum price."
        }

    products = (
        PenProduct.objects
        .filter(
            price__gte=start,
            price__lte=end
        )
        .values(
            "id",
            "name",
            "price",
            "scheme",
            "quantity_condition"
        )[:10]
    )

    products = list(products)

    if not products:
        return {
            "success": False,
            "message": f"No products found between ₹{start} and ₹{end}."
        }

    return {
        "success": True,
        "min_price": start,
        "max_price": end,
        "products": products
    }

def get_products_around_said_price(
    price: float,
    tolerance: float = 5
):

    min_price = max(0, price - tolerance)
    max_price = price + tolerance

    products = (
        PenProduct.objects
        .filter(
            price__gte=min_price,
            price__lte=max_price
        )
        .values(
            "id",
            "name",
            "price",
            "scheme",
            "quantity_condition"
        )[:10]
    )

    products = list(products)

    if not products:
        return {
            "success": False,
            "message": (
                f"No products found around ₹{price}."
            )
        }

    return {
        "success": True,
        "requested_price": price,
        "price_range": {
            "min": min_price,
            "max": max_price
        },
        "products": products
    }


def get_product_with_discount():

    products = (
        PenProduct.objects
        .exclude(scheme="No Scheme")
        .values(
            "id",
            "name",
            "price",
            "scheme",
            "quantity_condition"
        )[:10]
    )

    products = list(products)

    if not products:
        return {
            "success": False,
            "message": "There are currently no products with a discount or scheme."
        }

    return {
        "success": True,
        "products": products
    }


def get_product_images(product_id: int):

    try:

        product = (
            PenProduct.objects
            .prefetch_related("images")
            .get(id=product_id)
        )

    except PenProduct.DoesNotExist:

        return {
            "success": False,
            "message": "Product not found."
        }

    images = [
        image.image.url
        for image in product.images.all()
        if image.image
    ]

    if not images:

        return {
            "success": True,
            "product_id": product.id,
            "product_name": product.name,
            "images": [],
            "message": "No images are available for this product."
        }

    return {
        "success": True,
        "product_id": product.id,
        "product_name": product.name,
        "images": images
    }


def create_order_entry(product_id: int, quantity: int):
    
    

    if quantity <= 0:
        return {
            "success": False,
            "message": "Quantity must be greater than zero."
        }

    try:

        product = PenProduct.objects.get(
            id=1
        )

    except PenProduct.DoesNotExist:

        return {
            "success": False,
            "message": "Product does not exist."
        }

    total_price = product.price * quantity

    try:

        # order = OrderDetails.objects.create(
        #     product_id=product.id,
        #     quantity=quantity
        # )

        return {
            "success": True,
            "order": {
                # "order_id": order.id,
                "product_id": product.id,
                "product_name": product.name,
                "quantity": quantity,
                "unit_price": product.price,
                "total_price": total_price,
                "scheme": product.scheme,
                "quantity_condition": product.quantity_condition,
            },
            "message": "Order created successfully."
        }

    except Exception as e:

        print("ORDER ERROR:", str(e))

        return {
            "success": False,
            "message": "Unable to create the order."
        }

def send_email(
    subject,
    body,
    image_urls=None,
):
    if not subject:
        return {
            "success": False,
            "message": "Email subject is required."
        }

    if not body:
        return {
            "success": False,
            "message": "Email body is required."
        }

    if image_urls is None:
        image_urls = []

    if not isinstance(image_urls, list):
        return {
            "success": False,
            "message": "image_urls must be a list."
        }

    try:
        task = send_email_task.delay(
            to_email="diyasarkar0104@gmail.com",
            subject=subject,
            body=body,
            image_urls=image_urls,
        )

        return {
            "success": True,
            "message": "Email has been queued successfully.",
            "task_id": task.id,
            "to_email": "diyasarkar0104@gmail.com",
        }

    except Exception as e:
        return {
            "success": False,
            "message": "Unable to queue email.",
            "error": str(e),
        }



    
# def send_email(
#     to_email,
#     subject,
#     body,
#     image_urls=None,
# ):
#     """
#     Generic email function.

#     Can be used for:
#     - order confirmation
#     - product information
#     - product images
#     - discount information
#     - other product-related emails
#     """

#     if not to_email:
#         return {
#             "success": False,
#             "message": "Recipient email is required."
#         }

#     if not subject:
#         return {
#             "success": False,
#             "message": "Email subject is required."
#         }

#     if not body:
#         return {
#             "success": False,
#             "message": "Email body is required."
#         }

#     if image_urls is None:
#         image_urls = []

#     if not isinstance(image_urls, list):
#         return {
#             "success": False,
#             "message": "image_urls must be a list."
#         }

#     try:

#         task = send_email_task.delay(
#             to_email="diyasarkar0104@gmail.com",
#             subject=subject,
#             body=body,
#             image_urls=image_urls,
#         )

#         return {
#             "success": True,
#             "message": "Email has been queued successfully.",
#             "task_id": task.id,
#             "to_email": "diyasarkar0104@gmail.com",
#         }

#     except Exception as e:

#         return {
#             "success": False,
#             "message": "Unable to queue email.",
#             "error": str(e),
#         }