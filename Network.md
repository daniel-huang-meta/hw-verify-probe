```mermaid```
flowchart LR
    %% 外部网络区域 (External Networks)
    GH(("☁️ GitHub\n(External / Public)"))
    Manifold(("🌐 Manifold Platform\n(External Data Sink)"))

    %% 办公与路由核心
    WL["💻 Working Laptop\n(self-hosted runner)"]
    Router{"🖧 Local Router\n(192.168.1.0/24)"}

    GH --- WL --- Router

    %% 本地测试子网 1
    subgraph Subnet1 [Test Station 1]
        M1["🖥️ MacMini 1\n(192.168.1.101)"] -- "Local 192.168.2.x" --> B1["📦 Box 1"]
    end

    %% 本地测试子网 2
    subgraph Subnet2 [Test Station 2]
        M2["🖥️ MacMini 2\n(192.168.1.102)"] -- "Local 192.168.2.x" --> B2["📦 Box 2"]
    end

    %% 本地测试子网 3 (已恢复为普通节点)
    subgraph Subnet3 [Test Station 3]
        M3["🖥️ MacMini 3\n(192.168.1.103)"] -- "Local 192.168.2.x" --> B3["📦 Box 3"]
    end

    %% 新增纯数据处理节点 4 (不连 Box)
    subgraph Subnet4 [Data Upload Station]
        M4["🖥️ MacMini 4\n(192.168.1.104)"]
    end

    %% 办公网连线
    Router --> M1
    Router --> M2
    Router --> M3
    Router --> M4

    %% 外部数据上报连线 (仅限 MacMini 4)
    M4 == "Product Subnet 10.23.24.x\n(External Upload Route)" ===> Manifold

    %% 样式定义
    classDef external fill:#f8f9fa,stroke:#adb5bd,stroke-width:2px,stroke-dasharray: 5 5
    classDef office fill:#e7f5ff,stroke:#74c0fc,stroke-width:2px
    classDef special fill:#fff3cd,stroke:#f5c211,stroke-width:2px
    
    class GH,Manifold external
    class WL,Router,M1,M2,M3,B1,B2,B3 office
    class M4 special
