const cache = new Set();
onconnect = (event) => {
    const port = event.ports[0];

    const request = indexedDB.open('GeofieldDatabase');

    request.onerror = () => {
        console.error("Error: Permission to open a database has been denied.", request.error);
    };

    request.onupgradeneeded = () => {
        const db = request.result;
        if (!db.objectStoreNames.contains('coordinates')) {
            db.createObjectStore('coordinates', { keyPath: 'feature_id' });
        }
    };

    request.onblocked = () => {

    };

    request.onsuccess = () => {
        const db = request.result;

        db.onversionchange = () => {
            db.close();
            alert('Database is outdated. Please reload the page.');
        };

        db.onerror = (e) => {
            console.log("Error", e.target.error);
        }

        port.onmessage = async (e) => {
            const { data, _id, csrftoken, method } = e.data;
            if ( method === "GET" ) {
                let features = [];
                let objectStore = db.transaction('coordinates').objectStore('coordinates');
                objectStore.openCursor().onsuccess = (event) => {
                    const cursor = event.target.result;
                    if (cursor) {
                        features.push(cursor.value);
                        cursor.continue();
                    } else {
                        features = features.map((element) => {
                            return {
                                'geometry': element.geometry,
                                'id': element.feature_id,
                                'properties': {},
                                'type': 'Feature',
                            }
                        });
                        port.postMessage({ 'type': 'FeatureCollection', features });
                    }
                };

            } else if ( method === "POST" ) {
                const formattedData = data.features.map((feature) => {
                    return {
                        'feature_id': feature.id,
                        'geometry': feature.geometry,
                    }
                });
    
                const transaction = db.transaction('coordinates', 'readwrite');
                let objectStore = transaction.objectStore('coordinates');
                formattedData.forEach(feature => {
                    cache.add(feature.feature_id);
                    objectStore.put(feature);
                });
    
                transaction.oncomplete = () => {
                    port.postMessage(data);
                };
            }

            // synchronise(db, csrftoken, _id)
            // .catch(err => {
            //     console.error(err);
            // })

        };
    };

    const synchronise = async (db, csrftoken, id) => {
        // await sleep(1);
        return new Promise((resolve, reject) => {
            if (cache.size > 10) {
                let response = null;
                let objectStore = db.transaction('coordinates').objectStore('coordinates');
                objectStore.getAll().onsuccess = async (event) => {
                    const features = event.target.result;
                    response = await fetch(`/users/${id}/coordinates`, {
                        method: 'POST',
                        body: JSON.stringify({ features }),
                        headers: {
                            'Accept': 'application/json',
                            'Content-Type': 'application/json',
                            'X-Requested-With': 'XMLHttpRequest',
                            "X-CSRFToken": csrftoken,
                        },

                    }).then(res => {
                        if (!res.ok) {
                            throw new Error(res.statusText);
                        }
                        return res.json();
                    });
                }
                if (response) {
                    objectStore = db.transaction('coordinates', 'readwrite').objectStore('coordinates');
                    objectStore.clear();
                    cache.clear();
                    resolve();
                }
            } else {
                reject("Cache not yet full!!!");
            }
        });
    };

    const sleep = (ms) => {
        return new Promise(resolve => {
            const timeoutId = setTimeout(() => {
                clearTimeout(timeoutId);
                resolve();
            }, ms);
        });
    }
};