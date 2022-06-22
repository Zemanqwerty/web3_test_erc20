document.onclick = function(event){
    event = event || window.event;
    if (!event.target) {
        event.target = event.srcElement;
    }
}

async function updateStatus () {
    const Contract = event.target.id;
    console.log(event.target.className);

    let c_arr = Contract.split(" ");

    const one_eth = 1000000000000000000;

    let usd_count = Number(c_arr[1]) * Number(c_arr[2]);
    

    let transactionValue = one_eth * (usd_count / Number(c_arr[3]));

    if (transactionValue % 1 !== 0) {
        transactionValue += 0.5;
    };

    let params = [{
        "from": window.userWalletAddress,
        "to": c_arr[0],
        "gas": Number(21000).toString(16),
        "gasPrice": Number(2500000).toString(16),
        "value": Number(transactionValue).toString(16),
    }];

    let transactionResponse = await window.ethereum.request({method: "eth_sendTransaction", params});

    const response = await fetch("/admin/send_transaction_to_user", {
        "method": "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        "body": JSON.stringify({
            "transaction_id": c_arr[4],
        })
    })

    const json = await response.json()

    if (json["status"] == "success") {
        console.log('success status update')
    }
}

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
}

connectWallet()
