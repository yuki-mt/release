const { RTMClient } = require('@slack/rtm-api');
const token = 'xoxp-xxx'
const fs = require('fs');

const rtm = new RTMClient(token);
// const message = fs.readFileSync('bot_reply.txt', 'utf-8');
 const message = 'auto reply message'

const whiteLists = [
  'Dxxx', // UserID
];

(async () => {
  await rtm.start();
  rtm.on('message', (event) => {
    if (event.channel.startsWith('D') && event.type == 'message') {
      if (whiteLists.includes(event.channel))
        return;
      if (event.text && event.text.match(/help|聞きたい|can you|can I|why|\?|？|か。?$/)) {
        rtm.sendMessage(message, event.channel);
        console.log(`channel: ${event.channel}\tmessage: ${event.text}`)
      }
    }
  });
})();
