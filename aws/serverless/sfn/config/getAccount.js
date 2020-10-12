// getAccount.js

// get Account id using profile name
let AWS = require("aws-sdk");
const sts = new AWS.STS();
profile='';

module.exports.getAccountId = async () => {
    AWS.config.credentials = new AWS.SharedIniFileCredentials({profile: profile});
    // Checking AWS user details
    const {Account} = await sts.getCallerIdentity().promise();
    return Account;
};



