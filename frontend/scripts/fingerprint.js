async function getVisitorId() {
    try {
        const FingerprintJS = await import('https://openfpcdn.io/fingerprintjs/v4');
        const fp = await FingerprintJS.load();
        const result = await fp.get();
        const visitorId = result.visitorId;
        return {
            "status": "Success",
            "visitorId": visitorId,
        };
    } catch (error) {
        throw error
    }
}
