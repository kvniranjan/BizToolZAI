const fs = require('fs');
const admin = require('firebase-admin');
const serviceAccount = require('./serviceAccountKey.json');

if (!admin.apps.length) {
    admin.initializeApp({
      credential: admin.credential.cert(serviceAccount)
    });
}
const db = admin.firestore();

async function run() {
  try {
      console.log("=== FIREBASE ACTIVITY REPORT ===");
      
      // 1. Check Subscribers
      const subSnap = await db.collection('subscribers').get();
      console.log(`\n📧 Email Subscribers: ${subSnap.size}`);
      if (!subSnap.empty) {
          subSnap.forEach(doc => {
              const data = doc.data();
              let date = data.createdAt && data.createdAt.toDate ? data.createdAt.toDate().toISOString() : 'Unknown Date';
              console.log(`   - ${data.email} | Source: ${data.source} | Joined: ${date}`);
          });
      }

      // 2. Check Tool Submissions (from the /submit-tool.html page)
      const toolSnap = await db.collection('tool_submissions').get();
      console.log(`\n🛠️ Tool Submissions: ${toolSnap.size}`);
      if (!toolSnap.empty) {
          toolSnap.forEach(doc => {
              const data = doc.data();
              let date = data.submittedAt && data.submittedAt.toDate ? data.submittedAt.toDate().toISOString() : 'Unknown Date';
              console.log(`   - ${data.toolName} (${data.category}) | Contact: ${data.contactEmail} | Date: ${date}`);
          });
      }

  } catch (e) {
      console.error('Error fetching data from Firebase:', e);
  }
}

run();
