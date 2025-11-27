# DNA 隐私保护

## 用户使用

### 命令
```bash
dna隐藏uid    # 开启隐私保护（默认）
dna显示uid    # 关闭隐私保护
dna隐私设置   # 查看当前设置
```

### 效果
- 开启：`UID 123****789`
- 关闭：`UID 1234567890123`

## 开发使用

### 命名规范
- **`uid`** - 原始完整 UID，用于 API 调用和数据库
- **`display_uid`** - 显示 UID，用于图片和消息

### 标准流程
```python
# 1. 获取uid
uid = await DNABind.get_uid_by_game(user_id, bot_id)

# 2. 获取display_uid
from DNAUID.utils import get_display_uid
display_uid = await get_display_uid(uid, user_id, bot_id)

# 3. API调用用uid
role_data = await dna_api.get_role_detail(cookie, uid, dev_code)

# 4. 显示用display_uid
await bot.send(f"UID: {display_uid}")
await get_avatar_title_img(ev, uid, name, display_uid=display_uid)
```

### 核心函数
```python
# 获取显示UID（位于 utils/privacy.py）
async def get_display_uid(uid: str, user_id: str, bot_id: str) -> str

# 检查隐私设置
async def check_uid_privacy(uid: str, user_id: str, bot_id: str) -> bool
```

### 使用对照
| 场景 | 使用 |
|------|------|
| API 调用 | `uid` |
| 数据库操作 | `uid` |
| 图片生成 | `display_uid` |
| 文本消息 | `display_uid` |

## 技术实现

- **核心文件**：`utils/privacy.py`
- **数据库字段**：`DNAUser.hide_uid`（默认=1）
- **覆盖场景**：所有作图、登录、绑定消息
- **安全保证**：显示与业务完全分离

隐私保护仅影响显示，不影响业务功能。
