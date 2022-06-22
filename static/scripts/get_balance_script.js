const ethBalance_value = document.getElementById("eth_balance_value");

// window.onload = function() {
//     provider = new ethers.providers.Web3Provider(window.ethereum);
//     console.log(provider)
// }

const erc20ABI = [
    {
        "constant": true,
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "name": "_spender",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "name": "_from",
                "type": "address"
            },
            {
                "name": "_to",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "transferFrom",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "name": "",
                "type": "uint8"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [
            {
                "name": "_owner",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "name": "balance",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "name": "_to",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [
            {
                "name": "_owner",
                "type": "address"
            },
            {
                "name": "_spender",
                "type": "address"
            }
        ],
        "name": "allowance",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "payable": true,
        "stateMutability": "payable",
        "type": "fallback"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": true,
                "name": "spender",
                "type": "address"
            },
            {
                "indexed": false,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Approval",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "name": "from",
                "type": "address"
            },
            {
                "indexed": true,
                "name": "to",
                "type": "address"
            },
            {
                "indexed": false,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    }
];

async function getBalance() {
    const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' })

    .catch((e) => {
        console.error(e.message)

        error
    })

    if (!accounts) { return }

    window.userWalletAddress = accounts[0];

    const eth_Address = "0x407d73d8a49eeb85d32cf465507dd71d507100c1";
    console.log(window.userWalletAddress)

    let ethBalance = await window.ethereum.request({
        method: "eth_getBalance",
        params: [
            String(window.userWalletAddress),
            'latest'
        ]
    }).catch((err) => {
        console.log(err)
    });

    console.log(parseInt(ethBalance) / Math.pow(10, 18));
    console.log(ethBalance);

    let ethBalance_parsed = parseInt(ethBalance) / Math.pow(10, 18);

    ethBalance_value.innerText = ethBalance_parsed;
}

async function connectWallet() {
    const WalletTemplateText = document.getElementById("walletAddressText");
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
getBalance()