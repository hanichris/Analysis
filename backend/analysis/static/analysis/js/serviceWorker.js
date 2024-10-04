self.addEventListener('sync', (event) => {
    if (event.tag === 'synchronize') {
        self.console.log('Synchronizing data with the server.');
        event.waitUntil(syncDataToServer());
    }
});

self.addEventListener('message', (event) => {
    const data = JSON.parse(event.data);
    self.token = data.token;
    self.id = data.id;
})

async function syncDataToServer() {
    return new Promise((resolve, reject) => {
        const dbRequest = indexedDB.open('GeofieldDatabase');
        dbRequest.onsuccess = () => {
            const db = dbRequest.result;
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
                        const response = await fetch(`/users/${self.id}/coordinates`, {
                            method: 'POST',
                            body: JSON.stringify({ features }),
                            headers: {
                                'Accept': 'application/json',
                                'Content-Type': 'application/json',
                                'X-Requested-With': 'XMLHttpRequest',
                                "X-CSRFToken": self.token,
                            },
            
                        }).then(res => {
                            if (!res.ok) {
                                throw new Error(res.statusText);
                            }
                            return res.json();
                        }).catch(err => {
                            self.console.error('Error: ', err);
                            reject(err);
                        });
                        if (response) {
                            objectStore = db.transaction('coordinates', 'readwrite').objectStore('coordinates');
                            objectStore.clear();
                            self.console.log(response);
                            resolve(response);
                        }
                    } else {
                        reject('No data to synchronize the server with');
                    }
                }
            };
        }
    })
}