const WalletTemplateText = document.getElementById("walletAddressText");
const jsonResponseHTML = document.getElementById("json_respose");
const projectSmartContract = document.getElementById("smrt_contract").textContent.trim();
const projectName = document.getElementById("project").textContent.trim();

console.log("pn = "+ projectName, "sm = " + projectSmartContract);


async function send_transaction() {
    let coinsCount = document.getElementById("coins_count").value;
    let cur_ethPrice = document.getElementById("cur_eth_price").textContent;
    let cur_coinPrice = document.getElementById("coin_price").textContent;
    const one_eth = 1000000000000000000;

    let usd_count = Number(coinsCount) * Number(cur_coinPrice);
    
    let transactionValue = one_eth * (usd_count / Number(cur_ethPrice));

    if (transactionValue % 1 !== 0) {
        transactionValue += 0.5;
    };

    let params = [{
        "from": window.userWalletAddress,
        "to": "0x08807862D4B1be59401b208FbB9E5A4356AE3211",
        "gas": Number(21000).toString(16),
        "gasPrice": Number(2500000).toString(16),
        "value": Number(transactionValue).toString(16),
    }];

    let transactionResponse = await window.ethereum.request({method: "eth_sendTransaction", params});

    const apiResponse = await fetch("/api/create_new_transaction", {
        "method": "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        "body": JSON.stringify({
            "project_address": projectSmartContract,
            "coins_count": coinsCount,
            "project_name": projectName,
            "wallet": window.userWalletAddress,
        })
    });

    const json = await apiResponse.json();
    
    if (json["status"] == "success") {
        
        jsonResponseHTML.innerText = json["message"];
    }
    else{
        // const alertText = document.getElementById('alertText')
        // alertText.innerText = json["message"]
        
        console.log(json["status"], json["message"])
    }
};


async function connectWallet() {
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
}

connectWallet()

// send_transaction()