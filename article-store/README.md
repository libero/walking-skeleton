# Article Store

An XML data store for the Libero Walking skeleton.

## Endpoints
`GET`

`/articles`

Returns list of article ids.

```{xml}
<libero:articles xmlns:libero="http://libero.pub">
    <libero:article>0065-1737-azm-31-03-0367</libero:article>
    <libero:article>0034-1234-azm-32-04-0777</libero:article>
    <libero:article>0067-1777-azm-34-08-0237</libero:article>
</libero:articles>
```

Example:

`curl -v http://localhost:8000/articles -X GET`

---------------------

`DELETE`

`/articles/<article_id>/versions`

Deletes an entire article including all versions and content.

Example:

`curl -v http://localhost:8000/articles/0065 -X DELETE`

---------------------

`POST`

`/articles/<article_id>/versions`

Creates an article version, can include content items. If an article does
not yet exist, it will be created.

You cannot specify a version, the next version for the target article with be used
based on it's existing versions.

Example:

`curl -v -d '<root>...' http://localhost:8000/articles/0065 -X POST`

Payload:
```{xml}
<root>
    <content-list>
        <list-item>
            <language>en</language>
            <name>front</name>
            <model>http://localhost:8081/schemas/scielo/article/front.rng</model>
            <content>
                <front xmlns="http://libero.pub" xmlns:scielo="http://scielo.org" xml:lang="en">
                    <id>0065-1737-azm-31-03-0367</id>
                    <title>FOOBAR 9999 (Lepidoptera: Tortricidae) (Heinrich),
                        structural parameters and natural regeneration </title>
                    <abstract id="abstract">
                        <p>Foo</p>
                    </abstract>
                </front>
            </content>
        </list-item>
        <list-item>
            <language>en</language>
            <name>body</name>
            <model>http://localhost:8081/schemas/scielo/article/front.rng</model>
            <content>
                <body xmlns="http://libero.pub" xmlns:scielo="http://scielo.org" xml:lang="en">
                    <p>Foo</p>
                </body>
            </content>
        </list-item>
    </content-list>
</root>
```

---------------------
`PUT` `DELETE`

`/articles/<article_id>/versions/<version>`

`PUT` Update an article version, can include content items. Same payload
structure as the create but it will overwrite all existing content for
that version.

Example:

`curl -v -d '<root>...' http://localhost:8000/articles/0065/1 -X PUT`

`Delete` All versions including and greater than the specified version will be deleted.

Example:

`curl -v http://localhost:8000/articles/0065/1 -X DELETE`

---------------------
`GET`

`/articles/<article_id>/versions/<version>/<part>`

Return a specific `part` (e.g. front or body) of article content for a specified version.

Note: you can use the keyword `latest` as the version to get the latest
available version.

Examples:

`curl -v http://localhost:8000/articles/0065/1/front -X GET`

`curl -v http://localhost:8000/articles/0065/latest/body -X GET`


## Admin Interface

#### Create an admin user
To create the first user for the admin interface run the following command:

`docker-compose run article-store pipenv run python manage.py createsuperuser`

Then enter your desired username, email and password.

You can then access: `/admin` to log in.