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

---------------------

`DELETE`

`/articles/<article_id>`

Deletes an entire article including all versions and content.

---------------------

`POST` `PUT` `DELETE`

`/articles/<article_id>/<version>`

`POST` Create an article version, can include content items.

Example payload:

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

`PUT` Update an article version, can include content items. Same payload
structure as the create but it will overwrite all existing content for
that version.

`Delete` All versions including and greater than the specified version will be deleted.

---------------------
`GET`

`/articles/<article_id>/<version>/<part>`

Return a specific `part` (e.g. front or body) of article content for a specified version.




