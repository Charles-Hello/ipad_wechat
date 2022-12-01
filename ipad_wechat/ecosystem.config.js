module.exports = {
    apps: [{
        name: "ipad协议微信",
        version: "0.0.1",
        cwd: "..",
        script: "python",
        args: "-m ipad协议微信",
        autorestart: true,
        watch: ["ipad协议微信"],
        ignore_watch: [
            "ipad协议微信/*.log",
            "ipad协议微信/*/*.log",
            "ipad协议微信/requirements.txt",
            "ipad协议微信/ecosystem.config.js"
        ],
        watch_delay: 15000,
        interpreter: ""
    }]
}
