const cache = new Set();
const THRESHOLD = 10;
onconnect = (event) => {
    const port = event.ports[0];

    const request = indexedDB.open('GeofieldDatabase');

    request.onerror = () => {
        console.error("Error: Permission to open a database has been denied.", request.error);
    };

    request.onupgradeneeded = () => {
        const db = request.result;
        if (!db.objectStoreNames.contains('coordinates')) {
            db.createObjectStore('coordinates', { autoIncrement: true });
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
            const { data, _id, csrftoken, action } = e.data;
            if ( action === "getFeatures" ) {
                let features = [];
                const storeCache = new Set();
                let objectStore = db.transaction('coordinates').objectStore('coordinates');
                objectStore.openCursor(null, 'prev').onsuccess = (event) => {
                    const cursor = event.target.result;
                    if (cursor) {
                        const value = cursor.value;
                        if (!storeCache.has(value.feature_id)) {
                            storeCache.add(value.feature_id);
                            features.push(value);
                        }
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

            } else if ( action === "addFeatures" ) {
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
                    objectStore.add({...feature, 'synchronized': false});
                });
    
                transaction.oncomplete = () => {
                    port.postMessage(data);
                };

                if (cache.size >= THRESHOLD) {
                    syncDataToServer(db, csrftoken, _id)
                    .then(() => {
                        objectStore = db.transaction('coordinates', 'readwrite').objectStore('coordinates');
                        objectStore.clear();
                        cache.clear();
                    })
                    .catch(err => console.error(err));
                }
            } else if ( action === "syncData" ) {
                syncDataToServer(db, csrftoken, _id)
                .then(() => {
                    objectStore = db.transaction('coordinates', 'readwrite').objectStore('coordinates');
                    objectStore.clear();
                    cache.clear();
                })
                .catch(err => console.error(err));
            }
        };
    };
};

const syncDataToServer = async (db, csrftoken, id) => {
    return new Promise((resolve, reject) => {
        let features = [];
        const storeCache = new Set();
        let objectStore = db.transaction('coordinates').objectStore('coordinates');
        objectStore.openCursor(null, 'prev').onsuccess = async (event) => {
            const cursor = event.target.result;
            if (cursor) {
                let value = cursor.value;
                if (!storeCache.has(value.feature_id)) {
                    storeCache.add(value.feature_id);
                    features.push(value);
                }
                cursor.continue();
            } else {
                if (features.length > 0) {
                    const response = await fetch(`/users/${id}/coordinates`, {
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
                    resolve(response);
                } else {
                    reject('No data to synchronize the server with');
                }
            }
        }
    });
};