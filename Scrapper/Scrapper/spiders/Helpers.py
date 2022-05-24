def GetCategoryByProductName(self, value: str) -> str:
    if "iphone" in value.lower():
        return "Phone"
    elif "mac" in value.lower():
        return "Laptop"
    elif "ipad" in value.lower():
        return "Tablet"
    else:
        return "Other"
