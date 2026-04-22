flowchart LR
    %% 外部与核心网络
    GH(("☁️ github\n(External Network)"))
    WL["💻 Working Laptop\n(self-hosted runner)"]
    Router{"🖧 Router"}

    GH --- WL --- Router

    %% 子网 1
    subgraph Subnet1 [MacMini 1]
        M1["🖥️ MacMini 1\n(192.168.1.1)"] -- "192.168.2.x subnet" --> B1["📦 Box 1"]
    end

    %% 子网 2
    subgraph Subnet2 [MacMini 2]
        M2["🖥️ MacMini 2\n(192.168.1.2)"] -- "192.168.2.x subnet" --> B2["📦 Box 2"]
    end

    %% 子网 3 (新增 Manifold 平台连线)
    subgraph Subnet3 [MacMini 3]
        M3["🖥️ MacMini 3\n(192.168.1.3)"] -- "192.168.2.x subnet" --> B3["📦 Box 3"]
        M3 == "Product Subnet\n(Data Upload)" ==> Manifold(("📊 Manifold\n(Data Platform)"))
    end

    %% 路由连线
    Router -- "192.168.1.x" --> M1
    Router -- "192.168.1.x" --> M2
    Router -- "192.168.1.x" --> M3

    %% 样式定义
    classDef external fill:#f8f9fa,stroke:#dee2e6,stroke-width:2px
    classDef node fill:#e7f5ff,stroke:#74c0fc,stroke-width:2px
    classDef special fill:#fff3cd,stroke:#f5c211,stroke-width:2px
    
    class GH external
    class WL,Router,M1,M2,B1,B2 node
    class M3,B3,Manifold special
