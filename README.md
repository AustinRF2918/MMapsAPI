# Dependencies
	To install dependencies, run the following command in bash. This is assuming Python3 and pip3 is
	installed.

	Flask
	Flask-RESTful

# API

## Pin Hashes
Retrieve all pins stored on the backend.

**URL** : `/pins/hashes`

**Method** : `GET`

**Auth Required** : NO

**Body Params** : `None`

### Success Repsonses

**Code** : `200 OK`

**Content** : Pin hashes are returned so the local device can check for which pins it has and which it still needs.
```JSON
{
	"pin_hashes": [
		"29exdyxn883e9",
		"2083rnr09cf09",
		"8954c98cn5y02",
		"x90m0430m0c94",
		...
	]
}
```

---
## Pin
Retrieve certain pins given thier hashes.

**URL** : `/api/pins`

**Method** : `POST`

**Auth Required** : NO

**Body Params** :
```JSON
{
	"hashes": [
		"2083rnr09cf09",
		"x90m0430m0c94"
	]
}
```


### Success Repsonses

**Code** : `200 OK`

**Content** : Pin data representations are returned for each of the given valid hashes.
```JSON
{
	"pins": [
		{

		}
	]
}
```



---

`/decals`
{
	decals: [
		id: 6
	]
}

`/decals/6` -> returns actual image
