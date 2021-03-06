#!/usr/bin/env bash
set -e

function hold {
    read -n 1 -s -r -p "Press any key to continue"
    line
}

function line {
    echo -e "\n"
}

function wait_for_services {
    TIMEOUT="${2:-30}"
    echo "Waiting for services..."

    for ((i=1;i<=TIMEOUT;i++)); do
        STATUS_CODE=$(curl -o /dev/null --silent --head --write-out '%{http_code}' 'http://localhost:8085/articles')
        if [ "$STATUS_CODE" = "200" ]
        then
            break
        fi
        sleep 1
    done
}

function start {
    echo "Starting containers..."
    finish &> /dev/null
    docker-compose up --detach --renew-anon-volumes &> /dev/null
    wait_for_services
    echo "Done"
}

function finish {
    echo "Stopping containers..."
    docker-compose down --volumes &> /dev/null
    echo "Done"
}

trap finish EXIT

start

#
# Step 1: create article version 1
#

echo "First we'll create version 1 of article 1234"
hold

curl --verbose http://localhost:8085/articles/1234 -X POST --header 'Content-Type: application/xml' --data '
    <root>
        <content-list>
            <list-item>
                <language>en</language>
                <name>front</name>
                <content>
                    <front xmlns="http://libero.pub" xml:lang="en">
                        <id>1234</id>
                        <title>This is the title of the article</title>
                    </front>
                </content>
            </list-item>
            <list-item>
                <language>en</language>
                <name>body</name>
                <content>
                    <body xmlns="http://libero.pub" xml:lang="en">
                        <p>This is the body of the article.</p>
                        <image>
                            <title>An image</title>
                            <source height="497" width="620" media-type="image/png">http://private-assets-store/decoupled-architecture.png</source>
                        </image>
                    </body>
                </content>
            </list-item>
            <list-item>
                <language>es</language>
                <name>front</name>
                <content>
                    <front xmlns="http://libero.pub" xml:lang="es">
                        <id>1234</id>
                        <title>Este es el título del artículo</title>
                    </front>
                </content>
            </list-item>
        </content-list>
    </root>'

line
line
echo "Take a look at the Journal at http://localhost:8080, you'll see the article."
echo "Also take a look at the dashboard at http://localhost:8082, you'll see the history of the run."
hold

#
# Step 2: create article version 2
#

echo "Next we'll create version 2 of article 1234"
hold

curl --verbose http://localhost:8085/articles/1234/versions -X POST --header 'Content-Type: application/xml' --data '
    <root>
        <content-list>
            <list-item>
                <language>en</language>
                <name>front</name>
                <content>
                    <front xmlns="http://libero.pub" xml:lang="en">
                        <id>1234</id>
                        <title>This is the title of the article (version 2)</title>
                    </front>
                </content>
            </list-item>
            <list-item>
                <language>en</language>
                <name>body</name>
                <content>
                    <body xmlns="http://libero.pub" xml:lang="en">
                        <p>This is the body of the article (version 2).</p>
                        <image>
                            <title>An image</title>
                            <source height="497" width="620" media-type="image/png">http://private-assets-store/decoupled-architecture.png</source>
                        </image>
                    </body>
                </content>
            </list-item>
            <list-item>
                <language>es</language>
                <name>front</name>
                <content>
                    <front xmlns="http://libero.pub" xml:lang="es">
                        <id>1234</id>
                        <title>Este es el título del artículo (versión 2)</title>
                    </front>
                </content>
            </list-item>
        </content-list>
    </root>'

line
line
echo "Take a look at the Journal at http://localhost:8080, you'll see version 2 of the article."
echo "Also take a look at the dashboard at http://localhost:8082, you'll see the history of both runs."
hold

#
# Step 3: update article version 2
#

echo "Now we'll update version 2 of article 1234"
hold

curl --verbose http://localhost:8085/articles/1234/versions/2 -X PUT --header 'Content-Type: application/xml' --data '
    <root>
        <content-list>
            <list-item>
                <language>en</language>
                <name>front</name>
                <content>
                    <front xmlns="http://libero.pub" xml:lang="en">
                        <id>1234</id>
                        <title>This is the updated title of the article (version 2)</title>
                    </front>
                </content>
            </list-item>
            <list-item>
                <language>en</language>
                <name>body</name>
                <content>
                    <body xmlns="http://libero.pub" xml:lang="en">
                        <p>This is the updated body of the article (version 2).</p>
                        <image>
                            <title>A different image</title>
                            <source height="500" width="750" media-type="image/jpeg">http://private-assets-store/distracted.jpg</source>
                        </image>
                    </body>
                </content>
            </list-item>
            <list-item>
                <language>es</language>
                <name>front</name>
                <content>
                    <front xmlns="http://libero.pub" xml:lang="es">
                        <id>1234</id>
                        <title>Este es el título actualizado del artículo (versión 2)</title>
                    </front>
                </content>
            </list-item>
        </content-list>
    </root>'

line
line
echo "Take a look at the Journal at http://localhost:8080, you'll see the updated version 2 of the article."
echo "Also take a look at the dashboard at http://localhost:8082, you'll see the history of all 3 runs."
hold

#
# Step 4: delete article
#

echo "Finally, we'll delete article 1234"
hold

curl --verbose http://localhost:8085/articles/1234 -X DELETE

line
line
echo "Take a look at the Journal at http://localhost:8080, you'll see that the article has gone."
echo "Also take a look at the dashboard at http://localhost:8082, you'll see the history of all 4 runs."
hold

echo "Thanks for looking, this is now complete."
hold
