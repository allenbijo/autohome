# 🏠 AutoHome

**AutoHome** is a natural language-driven home automation system powered by [CrewAI](https://crewai.com). It translates your everyday commands — like _"Turn on the lights in the living room"_ or _"Dim the bedroom lights to 50%"_ — into direct, reliable control of your smart devices. No menus, no apps. Just talk, and your home listens.

## 🧠 How It Works

At its core, AutoHome uses **CrewAI**, an agent-based orchestration framework, to route and execute natural language instructions across a network of smart devices. Each device is abstracted as an intelligent agent with capabilities, memory, and autonomy.

AutoHome converts:
- 🗣️ Spoken or typed commands  
- 🔀 Into structured task chains  
- ⚙️ That interact with real/virtual devices (via APIs, protocols, or wrappers)

The system is modular, allowing new devices or actions to be plugged in with minimal overhead. Think of it as a universal translator between human intent and IoT logic.

## 🧩 Core Components

- **CrewAI Agents**: Specialized agents handle device-specific control (e.g., lights, thermostats, locks), and collaborate to execute multi-step tasks.
- **Task Parser**: Parses natural language input into intents and dispatches them to relevant agents.
- **Memory & Context**: Keeps track of prior commands to enable follow-up instructions like _"Make it warmer"_ or _"Turn that off."_
- **Device Abstraction Layer**: A unified interface for different brands/protocols — whether it's MQTT, REST, Zigbee, or smoke signals.

## 🪄 Example Interactions

```text
"Set the living room lights to 30% and play soft jazz."
→ [LightingAgent] dims the lights, [AudioAgent] plays jazz.

"Lock the front door and turn on the porch light if it's after sunset."
→ [TimeChecker] verifies condition, [SecurityAgent] locks door, [LightingAgent] turns on light.
```

## 💡 Use Cases

- Voice-activated home automation
- Smart routine orchestration ("Movie night", "Leaving home")
- Accessibility-focused control interfaces
- Experimental AI-agent powered environments

## 🚀 Philosophy

We believe smart homes should actually be _smart_ — not just app-controlled. AutoHome leverages AI not for show, but for genuinely intelligent, context-aware control. This is not your grandma's home automation system (unless your grandma is a prompt engineer).

---

## 📝 License

This project is licensed under the MIT License.  
See the [LICENSE](./LICENSE) file for full details.