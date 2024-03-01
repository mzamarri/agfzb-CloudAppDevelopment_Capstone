/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');
// const env = require('dotenv');
// env.config();
// console.log("process.env", process.env);

async function getDealerships(params) {
  console.log("params: ", params);
    const authenticator = new IamAuthenticator({ apikey: process.env.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
        authenticator: authenticator
    });
    let promise = new Promise((resolve, reject) => {
        cloudant.setServiceUrl(process.env.COUCH_URL);
        if (params.st) {
            // return dealership with this state
            console.log("getting by state")
            cloudant.postFind({db:'dealerships',selector:{st:params.st}})
            .then((result)=>{
                // console.log(result.result.docs);
                let code = 200;
                if (result.result.docs.length == 0) {
                    code = 404;
                }
                resolve({
                    statusCode: code,
                    headers: { 'Content-Type': 'application/json' },
                    body: result.result.docs
                });
            }).catch((err)=>{
                reject(err);
            })
        } else if (params.id) {
            // return dealership with this state
            console.log("getting by id")
            cloudant.postFind({
                db: 'dealerships',
                selector: {
                    id: parseInt(params.id)
                }
            })
            .then((result)=>{
                // console.log(result.result.docs);
                let code = 200;
                if (result.result.docs.length == 0) {
                    code = 404;
                }
                resolve({
                    statusCode: code,
                    headers: { 'Content-Type': 'application/json' },
                    body: result.result.docs[0]
                });
            }).catch((err)=>{
                reject(err);
            })
        } else {
            // return all documents
            console.log("getting all docs")
            cloudant.postAllDocs({ db: 'dealerships', includeDocs: true, limit: 10 })            
            .then((result)=>{
                console.log("result:", result);
                let code = 200;
                if (result.result.rows.length == 0) {
                    code = 404;
                }
                 resolve({
                    statusCode: code,
                    headers: { 'Content-Type': 'application/json' },
                    body: {result: result.result.rows}
                });
            }).catch((err)=>{
                reject(err);
            })
        }
    })
    let result = await promise;
    console.log("Promise result", result);
    return result;
}

// main({})

module.exports.main = getDealerships;