onconnect = (event) => {
    const port = event.ports[0];

    const request = indexedDB.open('GeofieldDatabase');

    request.onerror = () => {
        console.error(`Error: Permission to open a database has been denied.\n${request.error}`);
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

        port.onmessage = (e) => {
            const { data, _id, csrftoken } = e.data;
            const transaction = db.transaction('coordinates', 'readwrite');
            let objectStore = transaction.objectStore('coordinates');
            const formattedData = data.features?.map((feature) => {
                return {
                    'feature_id': feature.id,
                    'geometry': feature.geometry,
                }
            });

            formattedData.forEach(feature => {
                objectStore.put(feature);
            });

            transaction.oncomplete = () => {
                port.postMessage(data);
            };

            let features = [];
            objectStore = db.transaction('coordinates').objectStore('coordinates');
            objectStore.openCursor(null, 'prev').onsuccess = async (event) => {
                const cursor = event.target.result;
                if (cursor && features.length < 10) {
                    features.push(cursor.value);
                    cursor.continue();
                } else {
                    if (features.length == 10){
                        await fetch(`/users/${_id}/coordinates`, {
                            method: "POST",
                            body: JSON.stringify({
                                'features': features,
                            }),
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
                        }).catch(err => console.error(err));
                        flush = true;
                        features = [];
                    } else {
                        console.log('No more entries.');
                    }
                }
            }
        };
    };
};