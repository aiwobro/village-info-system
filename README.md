# 村庄信息管理系统

FastAPI + Vue 3 + PostgreSQL 的村庄信息管理平台。

## 功能模块

- 🔐 **用户认证** — JWT 登录注册
- 🏘️ **村庄管理** — 村庄信息维护
- 👥 **村民管理** — 村民档案、搜索、分页
- 📞 **联系方式** — 联系方式管理
- 🏦 **银行账户** — 银行账号管理
- 📦 **资产管理** — 村庄资产登记
- 🪵 **资源管理** — 村庄资源登记

## 技术栈

| 前端 | 后端 | 数据库 |
|------|------|--------|
| Vue 3 + Vite | FastAPI | PostgreSQL |
| TypeScript | SQLAlchemy | |
| Element Plus | Pydantic | |
| Pinia | JWT | |

## 本地开发

### 后端

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

## Docker 部署

```bash
# 构建并启动所有服务
docker compose up -d --build

# 查看状态
docker compose ps

# 查看日志
docker compose logs -f

# 停止服务
docker compose down
```

部署后访问 **http://localhost:8088**

默认管理员账号：`admin` / `admin123`

## API 文档

启动后访问：http://localhost:8088/api/v1/docs

## 项目结构

```
village-info-system/
├── backend/
│   ├── app/
│   │   ├── api/          # API 路由
│   │   ├── core/         # 核心配置
│   │   ├── crud/         # CRUD 操作
│   │   ├── models/       # SQLAlchemy 模型
│   │   └── schemas/      # Pydantic 模型
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/          # Axios 封装
│   │   ├── stores/       # Pinia 状态管理
│   │   ├── views/        # 页面组件
│   │   ├── router/       # Vue Router
│   │   └── main.ts
│   └── Dockerfile
├── nginx/
│   └── nginx.conf        # Nginx 配置
└── docker-compose.yml
```
