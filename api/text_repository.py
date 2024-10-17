app_description = {
    "title": "Tiny NMS",
    "description": """
            I know I haven't had time to do these two properly:
            * Exception handling
            * Meaningful response messages

            Having more time, I'd happily add those as well.
            """,
    "summary": "An Experimental Network Management Tool",
    "version": "0.0.1",
    "terms_of_service": "",
    "contact": {"url": "http://github.com/bazpya/nms", "email": "e@mail.com"},
    "license_info": {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
}

descriptions = {
    "id": "The unique identifier of the target device in integer format. Use 0 for experimental purposes.",
}

summaries = {
    "get_root": "Redirects to the Swagger page",
    "get_interfaces": "Retrieves list of all interfaces",
    "get_interfaces_loopback": "Retrieves list of loopback interfaces only",
    "post_interfaces_loopback": "Adds a loopback interface to the device. It automatically picks an unused number suffix for the new loopback",
    "delete_interfaces_loopback": "Deletes the loopback interface that has the specified number suffix",
}

tags_metadata = [
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]
