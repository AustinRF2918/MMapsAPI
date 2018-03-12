**NOTES**:
- Pin Images and Decal Images are separate (not the same things). Pin images are images of company logos. Decal images are things like birds, etc.

# Abstract Object
## Pin
- id                  : uuid (primary key)
- Description         : TEXT (TEXT Sql type)
- Address             : String
- Hash                : String
- Latitude            : Float
- Longitude           : Float
- Tags                : String array
- Image               : optional String (link to pin's img)
- PhoneNumber         : optional String
- Social              : optional List
  - Youtube_Link      : optional String
  - FB_Link           : optional String
  - Instagram_Link    : optional String
  - Pinterest_Link    : optional String
- Website_Link        : optional String
- Company_Data        : optional Dictionary (will be displayed in a modal view)
  - title             : String
  - message           : String
- PhotoStream...
- Is_Featured         : Bool


```JSON
{
  "pin": {
    "id": "78-78-78",
    "hash": 438098243089,
    "description": "Cool stuff here",
    "address": "123 Neato Street, MI",
    "lat": -14.12930,
    "long": -23.18293819,
    "tags": ["food", "coffee", "desert"],
    "logo_img_url": "https://azure.com/image/18309.png",
    "phone": "908910202",
    "social": [
      {
        "social_type": "facebook",
        "url": "..."
      },
      {
        "social_type": "instagram",
        "url": "..."
      }
    ],
    "website_url": "www.example.com",
    "company_data": {
      "title": "Coupon",
      "message": "Enter X for a free gift!"
    },
    "photo_stream": [
      "www.azure.com/images/1098230812.png",
      "www.azure.com/images/1231231241.png",
      "www.azure.com/images/80509458094.png",
      "www.azure.com/images/120930130.png"
    ],
    "Is_Featured": true
  }
}
```


## Decal (Images for user pins)
- link                : String (link to image blob)

*NOTE:* can only be created or deleted (no modify).

**Get decal links**
```JSON
{
  "decals": [
    "www.azure.com/6.png",
    "www.azure.com/6.png",
    "www.azure.com/6.png"
  ]
}
```
On Mobile: Go get the image and save locally with the url and image referenced together. That way can check if the image exists just by the url (using url as the id).
