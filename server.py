import os,json,requests
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voice_agent.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from fastmcp import FastMCP
from callapp.models.call_logic import *
from callapp.tasks import *
import time,datetime
import random
from logic_app.models import PenProduct
# from datetime import t timedelta
from django.utils import timezone
from django.core.cache import cache
from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import TokenVerifier, AccessToken
from dotenv import load_dotenv
load_dotenv()
mcp=FastMCP("WIN PEN")
AUTH_ID = os.getenv("AUTH_ID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
MCP_AUTH = os.getenv("MCP_AUTH_TOKEN")


# class SimpleTokenAuth(TokenVerifier):
#     async def verify_token(self, token: str) -> AccessToken:
#         print("verify_token()....:", token)
#         if token != MCP_AUTH:
#             raise ValueError("Invalid token")
            
#         return AccessToken(token=token, client_id="user", scopes=[])

# mcp = FastMCP(name="My Server", auth=SimpleTokenAuth())

@mcp.tool(
    description="""
    Resolve a product from product name.ALWAYS use this tool before any product-related action.
    Input:- product_name: name of the product given by user
    Output:- exact product_id
           - product details
    Never guess product_id manually.
    """
)
def get_product_info(product_name: str):
    print("get_product_info()")

    normalized_name = product_name.strip().lower()

    cache_key = f"product_resolve:{normalized_name}"

    cached_product = cache.get(cache_key)

    if cached_product:
        print("cachee")
        return cached_product

    product = (
        PenProduct.objects
        .filter(name__icontains=product_name)
        .only("id", "name", "price", "scheme")
        .first()
    )

    if not product:

        response = (
            "No product found. "
            "Please clarify the product name."
        )

        # Cache negative result
        cache.set(
            cache_key,
            response,
            timeout=86400
        )

        return response

    price = float(product.price)

    if product.scheme == "No Scheme":

        response = (
            f'{product.name} costs Rs.{price:g} '
            f'with no scheme. '
            f'Product ID is {product.id}.'
        )

    else:

        response = (
            f'{product.name} costs Rs.{price:g} '
            f'with scheme "{product.scheme}". '
            f'Product ID is {product.id}.'
        )

    print("PRODUCT ID:", product.id)

    # Save cache
    cache.set(
        cache_key,
        response,
        timeout=86400
    )

    return response

@mcp.tool(description="Get top ten products with details ,return only those data that has no scheme.")
def get_top_ten_products():
    print("get_top_ten_products()")
    cache_key = "top_ten_products_no_scheme"
    cached_response = cache.get(cache_key)
    # Return cache immediately
    if cached_response:
        return cached_response
    # Fallback DB query if cache empty
    data = (
        PenProduct.objects
        .filter(scheme="No Scheme")
        .values(
            "name",
            "price",

        )[:10]
    )
    formatted_products = []
    for item in data:
        price = float(item["price"])

        formatted_products.append(
            f'{item["name"]} Rs.{price:g}'
        )
    final_response = (
        ", ".join(formatted_products)
        + " — all with no scheme"
    )
    print(final_response)
    # Save cache
    cache.set(
        cache_key,
        final_response,
        timeout=None
    )
    
    return final_response

    

@mcp.tool(description="Get the product range,give range of min and max value eg:'Suggest me the product between range 5 to 15.'")
def get_products_by_range(start:int , end:int):
    print("get_products_by_range()")
    cache_key = f"products_range:{start}:{end}"
    cached_response = cache.get(cache_key)
    if cached_response:
        return cached_response
    data = (
        PenProduct.objects
        .filter(
            price__gte=start,
            price__lte=end
        )
        .values(
            "name",
            "price",
            "scheme",
            "quantity_condition"
        )[:10]
    )
    formatted_products = []
    for item in data:
        price = float(item["price"])

        if item["scheme"] == "No Scheme":

            formatted_products.append(
                f'{item["name"]} Rs.{price:g} '
                f'(No Scheme)'
            )

        else:

            formatted_products.append(
                f'{item["name"]} Rs.{price:g} '
                f'({item["scheme"]} on '
                f'{item["quantity_condition"]})'
            )

    final_response = " , ".join(formatted_products)

    cache.set(
        cache_key,
        final_response,
        timeout=86400
    )

    print("get_products_by_range->", final_response)

    return final_response

@mcp.tool(
    description="Get the product details that has no scheme"
)
def get_product_with_no_scheme():

    cache_key = "products:no_scheme"

    cached_response = cache.get(cache_key)

    if cached_response:
        return cached_response

    # Fallback DB query
    data = (
        PenProduct.objects
        .filter(scheme="No Scheme")
        .values(
            "name",
            "price"
        )[:10]
    )

    formatted_products = []

    for item in data:
        price = float(item["price"])

        formatted_products.append(
            f'{item["name"]} Rs.{price:g}'
        )

    final_response = (
        ", ".join(formatted_products)
        + " — all with no scheme"
    )

    # Save cache
    cache.set(
        cache_key,
        final_response,
        timeout=None
    )

    return final_response

@mcp.tool(description="Get the product details around specific price.eg:'Suggest me products around price 10.'")
def get_products_around_said_price(p:float):
    print("get_products_around_said_price()")

    cache_key = f"products_around_price:{p}"

    cached_response = cache.get(cache_key)

    if cached_response:
        return cached_response

    data = (
        PenProduct.objects
        .filter(price__gte=p)
        .values(
            "name",
            "price",
            "scheme",
            "quantity_condition"
        )[:10]
    )

    formatted_products = []

    for item in data:

        price = float(item["price"])

        if item["scheme"] == "No Scheme":

            formatted_products.append(
                f'{item["name"]} Rs.{price:g} '
                f'(No Scheme)'
            )

        else:

            formatted_products.append(
                f'{item["name"]} Rs.{price:g} '
                f'({item["scheme"]} on '
                f'{item["quantity_condition"]})'
            )

    final_response = " , ".join(formatted_products)

    cache.set(
        cache_key,
        final_response,
        timeout=86400
    )

    return final_response

@mcp.tool(description="Get the product details around specific price.eg:'Suggest me products with discounts'")
def get_product_with_discount():
    cache_key = "products_with_discount"

    cached_response = cache.get(cache_key)

    # Return cache if exists
    if cached_response:
        return cached_response

    # Fallback DB query
    data = (
        PenProduct.objects
        .exclude(scheme="No Scheme")
        .values(
            "name",
            "price",
            "scheme",
            "quantity_condition"
        )[:10]
    )

    formatted_products = []

    for item in data:
        price = float(item["price"])

        formatted_products.append(
            f'{item["name"]} Rs.{price:g} '
            f'({item["scheme"]} on {item["quantity_condition"]})'
        )

    final_response = " , ".join(formatted_products)

    # Save cache
    cache.set(
        cache_key,
        final_response,
        timeout=None
    )

    return final_response



@mcp.tool(description="For order entry customer needs to provide user id,product id and the quantity of the product buys.Take the user id from get_USER_ID.Please ask each time for confirmation before placing order")
def create_order_entry(user_id: int , prod_id :int , quantity: int):
    print("get_order_entry()")
    print({"user_id": user_id , "product_id":prod_id , "quantity":quantity})
    # Validate quantity
    if quantity <= 0:
        return "Quantity must be greater than 0"
    # Validate product
    if not PenProduct.objects.filter(id=prod_id).exists():
        return "Invalid product"
    try:
        OrderDetails.objects.create(
            user_id=user_id,
            product_id=prod_id,
            quantity=quantity
        )
        return "Order created successfully!"

    except Exception as e:
        print(str(e))
        return "Order creation failed"



@mcp.tool(description=f"Get the current time in this format YYYY-MM-DD HH:MM:SS")
def get_current_time():
    print(datetime.datetime.now())
    return f"current time is {datetime.datetime.now()}"




@mcp.tool(description="Fetch product image of the product name.Use resolve_product() function whenever user enquires for prodect related queires")
def get_product_images(product_id: int):
    print("get_product_images()")
    cache_key = f"product_images:{product_id}"
    cached_response = cache.get(cache_key)
    if cached_response:
         return cached_response
    try:
        product = (PenProduct.objects.prefetch_related("images").only("id", "name").get(id=product_id))
    except PenProduct.DoesNotExist:
        response = {"error": "Product not found"}
        cache.set(cache_key, response, timeout=300)
        return response
    image_urls = []
    for img in product.images.all():
        if img.image:
              image_urls.append(img.image.url)

    if not image_urls:
        response = {
            "product_id": product.id,
            "product": product.name,
            "images": [],
            "message": "No images found for this product"
        }
        cache.set(cache_key, response, timeout=3600)
        return response
    response = {
        "product_id": product.id,
        "product": product.name,
        "images": image_urls
    }
    cache.set(cache_key, response, timeout=86400)


@mcp.tool(
    description="""
    Universal Email Tool for DCS System.
    Handles ALL email types:
    - Order confirmation
    - Product information
    - Product images
    - General queries
    RULES:
    - If product_name is given → fetch product from DB
    - Attach images only if product exists AND user requests images
    - NEVER guess product_id
    - For order confirmation, include product details in instruction for email content including scheme and image if available
    INPUTS:
    - user_id: authenticated user
    - instruction: full user request
    - product_name (optional)
    """
)
def send_email_router(user_id: int, instruction: str, product_name: str = None):
    image_paths = []
    product = None
    print("instruction in send_email_router:", instruction)
    # STEP 1: product lookup
    if product_name:
        product = PenProduct.objects.prefetch_related("images").filter(
            name__icontains=product_name
        ).first()

        if product:
            image_paths = [
                img.image.path for img in product.images.all() if img.image
            ]

    # STEP 2: detect intent (simple but effective)
    text = instruction.lower()

    wants_images = any(x in text for x in ["image", "pic", "photo", "show"])
    wants_order = any(x in text for x in ["order", "confirm", "placed"])

    # STEP 3: build enhanced instruction
    if product:
        instruction += f"""
                    Product Context:
                    Name: {product.name}
                    Price: {product.price}
                    Scheme: {product.scheme}
                    Availability: {product.quantity_condition}
                    """
    print("instruction with/ without product context:", instruction)
    # STEP 4: decide attachments
    if not wants_images:
        image_paths = None

    # STEP 5: SINGLE CELERY CALL
    send_email_task.delay(user_id, instruction, image_paths)

    return {
        "success": True,
        "message": "Email queued successfully",
        "attachments": len(image_paths) if image_paths else 0
    }

