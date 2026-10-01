# products/ollama_tools.py

OLLAMA_TOOLS = [

    {
    "type": "function",
    "function": {
        "name": "get_all_products",
        "description": """
        Get the complete list of all available pen products.

        Use this tool ONLY when the customer explicitly asks for:
        - all products
        - all pens
        - every product
        - complete product list
        - entire product catalog

        Do NOT use this tool when the customer asks for:
        - top 10 products
        - a few products
        - products within a price range
        - products around a specific price
        - discounted products
        """,
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
},

    # ============================================================
    # 1. GET SPECIFIC PRODUCT
    # ============================================================

    {
        "type": "function",
        "function": {
            "name": "get_product_info",

            "description": """
            Find a specific product using the product name.

            Use this whenever the customer asks about a particular
            product, its price, scheme, quantity condition or details.

            Always use this tool instead of guessing product information.
            """,

            "parameters": {
                "type": "object",

                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": (
                            "The product name mentioned by the customer."
                        )
                    }
                },

                "required": [
                    "product_name"
                ]
            }
        }
    },


    # ============================================================
    # 2. TOP 10 PRODUCTS WITHOUT SCHEME
    # ============================================================

    {
        "type": "function",
        "function": {
            "name": "get_top_ten_products",

            "description": """
            Get up to 10 available products that have no scheme.

            Use this when the customer asks general questions such as:
            - What products do you sell?
            - Show me your products.
            - What pens are available?
            - Give me some products.

            Do not use this when the customer specifies a price range.
            """,

            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },


    # ============================================================
    # 3. PRODUCTS BY PRICE RANGE
    # ============================================================

    {
        "type": "function",
        "function": {
            "name": "get_products_by_range",

            "description": """
            Find products whose price is between a minimum and
            maximum price.

            Use this when the customer specifies a price range.

            Example:
            'Show me pens between 5 and 20 rupees.'
            'I need something between Rs.10 and Rs.50.'
            """,

            "parameters": {
                "type": "object",

                "properties": {

                    "start": {
                        "type": "integer",
                        "description": "Minimum price."
                    },

                    "end": {
                        "type": "integer",
                        "description": "Maximum price."
                    }

                },

                "required": [
                    "start",
                    "end"
                ]
            }
        }
    },


    # ============================================================
    # 4. PRODUCTS AROUND SPECIFIC PRICE
    # ============================================================

    {
        "type": "function",
        "function": {
            "name": "get_products_around_said_price",

            "description": """
            Find products around a price specified by the customer.

            Use this when the customer asks for products around
            a particular price.

            Examples:
            - Show me pens around Rs.10.
            - What can I get for around 20 rupees?
            - Suggest something around 50 rupees.
            """,

            "parameters": {
                "type": "object",

                "properties": {

                    "p": {
                        "type": "number",
                        "description": "Price specified by the customer."
                    }

                },

                "required": [
                    "p"
                ]
            }
        }
    },


    # ============================================================
    # 5. PRODUCTS WITH DISCOUNT / SCHEME
    # ============================================================

    {
        "type": "function",
        "function": {
            "name": "get_product_with_discount",

            "description": """
            Find products that have a scheme or discount.

            Use this when the customer asks:
            - Which products have discounts?
            - Do you have any offers?
            - Which pens have schemes?
            - Show me discounted products.
            - Are there any special offers?

            Do not use this for a specific product. For a specific
            product, use get_product_info.
            """,

            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },


    # ============================================================
    # 6. PRODUCT IMAGES
    # ============================================================

    {
        "type": "function",
        "function": {
            "name": "get_product_images",

            "description": """
            Get images of a specific product.

            Use this when the customer asks to:
            - Show me the product image.
            - Show me a picture.
            - Can I see the pen?
            - Send me the product photo.

            You need the product_id to call this tool.

            Never guess the product_id.

            First use get_product_info to identify the product and
            obtain its product_id.
            """,

            "parameters": {
                "type": "object",

                "properties": {

                    "product_id": {
                        "type": "integer",
                        "description": (
                            "The exact product ID returned by "
                            "get_product_info."
                        )
                    }

                },

                "required": [
                    "product_id"
                ]
            }
        }
    },


    # ============================================================
    # 7. CREATE ORDER
    # ============================================================

    {
    "type": "function",
    "function": {
        "name": "create_order_entry",
        "description": """
        Create the final order entry.

        IMPORTANT:
        This tool must ONLY be called after the customer has
        explicitly confirmed the order.

        Before calling this tool, the assistant MUST have:
        1. Identified the exact product using get_product_info.
        2. Obtained the exact product_id from get_product_info.
        3. Obtained the customer's desired quantity.
        4. Shown the product, quantity, price and total to the customer.
        5. Received explicit confirmation from the customer.

        NEVER guess the product_id.
        NEVER use a product name as the product_id.
        NEVER call this tool on the first request to buy a product.
        """,
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "integer",
                    "description":
                        "Exact product ID returned by get_product_info."
                },
                "quantity": {
                    "type": "integer",
                    "description":
                        "Exact quantity explicitly requested by the customer."
                }
            },
            "required": [
                "product_id",
                "quantity"
            ]
        }
    }
},

    # ============================================================
    # 8. send email
    # ============================================================
    {
    "type": "function",
    "function": {
        "name": "send_email",
        "description": (
            "Queue an email containing product, order, pricing, "
            "discount, or image information. "
            "For testing, the application uses a fixed recipient. "
            "Do not ask the customer for an email address."
        ),
        "parameters": {
            "type": "object",
            "properties": {

                "subject": {
                    "type": "string",
                    "description": "Subject of the email."
                },

                "body": {
                    "type": "string",
                    "description": (
                        "Complete plain-text information that should "
                        "be included in the email."
                    )
                },

                "image_urls": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": (
                        "Optional list of product image URLs."
                    )
                }
            },

            "required": [
                "subject",
                "body"
            ]
        }
    }
}
]