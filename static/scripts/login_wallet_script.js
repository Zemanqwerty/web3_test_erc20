window.userWalletAddress = null
const LoginButton = document.getElementById('LoginButton')
const WalletTemplateText = document.getElementById('walletAddressText')
// const UserWallet = document.getElementById('UserWallet')

function toggleButton() {
    if (!window.ethereum) {
        LoginButton.innerText = 'MetaMask isnt installed'

        return false
    }
    LoginButton.addEventListener('click', loginWithMetaMask)
}

async function loginWithMetaMask () {
    const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' })

    .catch((e) => {
        console.error(e.message)

        error
    })

    if (!accounts) { return }

    window.userWalletAddress = accounts[0];

    let walletAd = window.userWalletAddress;
    let up_wallet_address = "";

    for (var wallet_i in walletAd) {
        up_wallet_address += walletAd[wallet_i]
        
        if (wallet_i == 4) {
            break;
        };
    };

    up_wallet_address += "..." + walletAd[walletAd.length - 4] + walletAd[walletAd.length - 3] + walletAd[walletAd.length - 2] + walletAd[walletAd.length - 1]

    WalletTemplateText.innerText = up_wallet_address;

    LoginButton.removeEventListener('click', loginWithMetaMask);
    //   setTimeout(() => {
    //     LoginButton.addEventListener('click', signOutOfMetaMask)
    //   }, 200)
}

// function signOutOfMetaMask() {
//     window.userWalletAddress = null
//     // userWallet.innerText = ''
//     LoginButton.innerText = 'sign in'

//     LoginButton.removeEventListener('click', signOutOfMetaMask)
//     setTimeout(() => {
//       LoginButton.addEventListener('click', loginWithMetaMask)
//     }, 200)
//   }

  window.addEventListener('DOMContentLoaded', () => {
    toggleButton()
  });



async function sendGetRequest() {
    const searchRequest = document.getElementById("get_request_value");

    let requestValue = searchRequest.value;
    console.log(requestValue)

    if (requestValue != '') {
        window.location.replace("/?search=" + requestValue)
    }
    else {
        window.location.replace('/')
    }
}












// async function getBalance() {
//     // Request
//     const balance = await window.ethereum.request({"jsonrpc":"2.0",
//                                                     "method":"eth_getBalance",
//                                                     "params":
//                                                         ["0x55d398326f99059ff775485246999027b3197955",
//                                                         "latest"],
//                                                     "id":1})

//     .catch((e) => {
//         console.error(e.message)

//         error
//     })

//     console.log(balance)

// }

// async function viewCurProject() {
//     project_name = getElementById('')
// }