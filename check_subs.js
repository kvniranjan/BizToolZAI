const fs = require('fs');
const admin = require('firebase-admin');

const raw = fs.readFileSync('raw.json', 'utf8');
const obj = JSON.parse(raw);

// Fix the private key (spaces to newlines between headers)
let pk = obj.private_key;
let match = pk.match(/-----BEGIN PRIVATE KEY-----\s+(.*?)\s+-----END PRIVATE KEY-----/);
if (match) {
    let body = match[1].replace(/\s+/g, '\n');
    obj.private_key = `-----BEGIN PRIVATE KEY-----\n${body}\n-----END PRIVATE KEY-----\n`;
}
fs.writeFileSync('serviceAccountKey.json', JSON.stringify(obj, null, 2));

const serviceAccount = require('./serviceAccountKey.json');
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

const db = admin.firestore();

async function run() {
  try {
      const snapshot = await db.collection('subscribers').get();
      if (snapshot.empty) {
        console.log('No subscribers found in database.');
        return;
      }
      console.log(`Found ${snapshot.size} subscribers in Firestore:\\n`);
      snapshot.forEach(doc => {
        const data = doc.data();
        let date = 'Unknown';
        if (data.createdAt) {
           date = data.createdAt.toDate ? data.createdAt.toDate().toISOString() : data.createdAt;
        }
        console.log(`Email: ${data.email} | Source: ${data.source || 'Direct'} | Date: ${date}`);
      });
  } catch (e) {
      console.error('Error fetching subscribers:', e);
  }
}

run();
