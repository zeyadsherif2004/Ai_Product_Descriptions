2025-09-29T04:11:42.936534124Z ==> Uploading build...
2025-09-29T04:12:05.811981738Z ==> Uploaded in 17.5s. Compression took 5.4s
2025-09-29T04:12:05.903052554Z ==> Build successful 🎉
2025-09-29T04:12:12.699087844Z ==> Deploying...
2025-09-29T04:12:51.658094568Z ==> Running '  cd backend && python fix_database.py && python run_migrations.py && uvicorn src.main:app --host 0.0.0.0 --port $PORT'
2025-09-29T04:12:58.039539926Z 🔧 Database Fix Script
2025-09-29T04:12:58.039569466Z ==================================================
2025-09-29T04:12:58.039576207Z ✅ Found database URL: postgresql://ai_descriptions_db_user:ijlatK7LezNTw...
2025-09-29T04:12:58.039579827Z ✅ Database connection established
2025-09-29T04:12:58.039582657Z 🔄 Creating subscriptions table...
2025-09-29T04:12:58.039585497Z 🔄 Creating indexes...
2025-09-29T04:12:58.039587947Z 🔄 Creating webhook_events table...
2025-09-29T04:12:58.039590507Z 🔄 Creating transactions table...
2025-09-29T04:12:58.039593657Z 🔄 Creating usage table...
2025-09-29T04:12:58.039596177Z 🔄 Creating user_credits table...
2025-09-29T04:12:58.039598517Z ✅ All tables created successfully!
2025-09-29T04:12:58.039600967Z 🎉 Database fix completed successfully!
2025-09-29T04:13:05.212056008Z INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
2025-09-29T04:13:05.212082618Z INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
2025-09-29T04:13:05.212085608Z INFO  [alembic.runtime.migration] Will assume transactional DDL.
2025-09-29T04:13:05.212088168Z INFO  [alembic.runtime.migration] Will assume transactional DDL.
2025-09-29T04:13:05.392974796Z INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
2025-09-29T04:13:05.392998227Z INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
2025-09-29T04:13:05.393001997Z INFO  [alembic.runtime.migration] Will assume transactional DDL.
2025-09-29T04:13:05.393005287Z INFO  [alembic.runtime.migration] Will assume transactional DDL.
2025-09-29T04:13:05.402883884Z INFO  [alembic.runtime.migration] Running upgrade  -> 0001_initial, initial tables
2025-09-29T04:13:05.402900715Z INFO  [alembic.runtime.migration] Running upgrade  -> 0001_initial, initial tables
2025-09-29T04:13:05.989975918Z 🔄 Checking current database state...
2025-09-29T04:13:05.990000709Z 🔄 Running database migrations...
2025-09-29T04:13:05.990004929Z ⚠️ Migration error: (psycopg2.errors.DuplicateTable) relation "users" already exists
2025-09-29T04:13:05.990008969Z 
2025-09-29T04:13:05.990011569Z [SQL: 
2025-09-29T04:13:05.990014139Z CREATE TABLE users (
2025-09-29T04:13:05.99003861Z 	id VARCHAR NOT NULL, 
2025-09-29T04:13:05.99004219Z 	email VARCHAR, 
2025-09-29T04:13:05.99004619Z 	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
2025-09-29T04:13:05.99004901Z 	PRIMARY KEY (id)
2025-09-29T04:13:05.99005148Z )
2025-09-29T04:13:05.990053831Z 
2025-09-29T04:13:05.990056431Z ]
2025-09-29T04:13:05.990059031Z (Background on this error at: https://sqlalche.me/e/20/f405)
2025-09-29T04:13:05.990061991Z 🔄 Attempting to continue with existing schema...
2025-09-29T04:13:05.990065531Z ❌ Migration failed: cannot import name 'get_db' from 'src.database.connection' (/opt/render/project/src/backend/src/database/connection.py)
2025-09-29T04:13:05.990068171Z 🔄 Attempting to use simple database initialization...
2025-09-29T04:13:05.990071001Z 🔄 Initializing database...
2025-09-29T04:13:05.990073461Z ✅ Database initialized successfully!
2025-09-29T04:13:05.990075961Z ✅ Database initialized with simple script!
2025-09-29T04:13:16.668840226Z ==> No open ports detected, continuing to scan...
2025-09-29T04:13:16.892907235Z ==> Docs on specifying a port: https://render.com/docs/web-services#port-binding
2025-09-29T04:13:29.456847692Z /opt/render/project/src/.venv/lib/python3.13/site-packages/pydantic/_internal/_config.py:373: UserWarning: Valid config keys have changed in V2:
2025-09-29T04:13:29.456863692Z * 'schema_extra' has been renamed to 'json_schema_extra'
2025-09-29T04:13:29.456867742Z   warnings.warn(message, UserWarning)
2025-09-29T04:13:29.556674733Z INFO:     Started server process [56]
2025-09-29T04:13:29.556701644Z INFO:     Waiting for application startup.
2025-09-29T04:13:30.193114903Z INFO:     Application startup complete.
2025-09-29T04:13:30.194224935Z INFO:     Uvicorn running on http://0.0.0.0:10000 (Press CTRL+C to quit)
2025-09-29T04:13:30.249192363Z No .env file found at: /opt/render/project/src/backend/.env
2025-09-29T04:13:30.249218734Z Make sure to create a .env file with your GEMINI_API_KEY
2025-09-29T04:13:30.249222383Z ✅ Gemini API key loaded successfully
2025-09-29T04:13:30.249224874Z 📊 Using model: gemini-flash-latest, temperature: 0.8
2025-09-29T04:13:30.249243104Z 💰 Daily cost limit: $1.0, Monthly: $10.0
2025-09-29T04:13:30.249246294Z ✅ Gemini model 'gemini-flash-latest' configured successfully
2025-09-29T04:13:30.249248964Z ✅ AI Product Descriptions API started successfully
2025-09-29T04:13:30.249251515Z 🤖 Model: gemini-flash-latest (Live mode)
2025-09-29T04:13:30.249255184Z 🌡️  Temperature: 0.8
2025-09-29T04:13:30.249257815Z ✅ API key configured - ready for AI generation
2025-09-29T04:13:30.249260475Z 💳 Credit service initialized - rate limiting enabled
2025-09-29T04:13:30.249263455Z 📋 Subscription plans initialized
2025-09-29T04:13:30.249266465Z INFO:     127.0.0.1:36666 - "HEAD / HTTP/1.1" 404 Not Found
2025-09-29T04:13:33.440713323Z ==> Your service is live 🎉
2025-09-29T04:13:33.723093622Z ==> 
2025-09-29T04:13:33.804971661Z ==> ///////////////////////////////////////////////////////////
2025-09-29T04:13:33.883312891Z ==> 
2025-09-29T04:13:33.99677159Z ==> Available at your primary URL https://ai-product-descriptions.onrender.com
2025-09-29T04:13:34.073961369Z ==> 
2025-09-29T04:13:34.155520659Z ==> ///////////////////////////////////////////////////////////
2025-09-29T04:13:35.655369954Z INFO:     34.168.108.203:0 - "GET / HTTP/1.1" 404 Not Found
2025-09-29T04:14:10.620940271Z INFO:     156.204.156.48:0 - "WebSocket /ws/payments" [accepted]
2025-09-29T04:14:10.621312682Z INFO:     connection open
2025-09-29T04:14:10.715550801Z INFO:     156.204.156.48:0 - "OPTIONS /api/payment/user/credits HTTP/1.1" 200 OK
2025-09-29T04:14:10.716096307Z INFO:     156.204.156.48:0 - "OPTIONS /api/payment/user/credits HTTP/1.1" 200 OK
2025-09-29T04:14:10.717877449Z INFO:     156.204.156.48:0 - "OPTIONS /api/payment/user/subscription HTTP/1.1" 200 OK
2025-09-29T04:14:10.767425349Z INFO:     156.204.156.48:0 - "OPTIONS /api/payment/user/credits HTTP/1.1" 200 OK
2025-09-29T04:14:11.063911417Z INFO:     156.204.156.48:0 - "OPTIONS /api/payment/user/subscription HTTP/1.1" 200 OK
2025-09-29T04:14:11.153540293Z WARNING:src.payments.endpoints:🔍 No subscription found for user bpR6MB3823T20EK7BEa3cs2y22u2
2025-09-29T04:14:11.163623606Z WARNING:src.payments.endpoints:User bpR6MB3823T20EK7BEa3cs2y22u2 has no subscription record, returning free tier
2025-09-29T04:14:11.164294326Z INFO:     156.204.156.48:0 - "GET /api/payment/user/subscription HTTP/1.1" 200 OK
2025-09-29T04:14:11.391240222Z INFO:     156.204.156.48:0 - "GET /api/payment/user/credits HTTP/1.1" 200 OK
2025-09-29T04:14:11.403305193Z WARNING:src.payments.endpoints:🔍 No subscription found for user bpR6MB3823T20EK7BEa3cs2y22u2
2025-09-29T04:14:11.412996775Z WARNING:src.payments.endpoints:User bpR6MB3823T20EK7BEa3cs2y22u2 has no subscription record, returning free tier
2025-09-29T04:14:11.416889438Z INFO:     156.204.156.48:0 - "GET /api/payment/user/subscription HTTP/1.1" 200 OK
2025-09-29T04:14:11.56936754Z WARNING:src.payments.endpoints:🔍 No subscription found for user bpR6MB3823T20EK7BEa3cs2y22u2
2025-09-29T04:14:11.579438333Z WARNING:src.payments.endpoints:User bpR6MB3823T20EK7BEa3cs2y22u2 has no subscription record, returning free tier
2025-09-29T04:14:11.579722271Z INFO:     156.204.156.48:0 - "GET /api/payment/user/subscription HTTP/1.1" 200 OK
2025-09-29T04:14:11.604312896Z INFO:     156.204.156.48:0 - "GET /api/payment/user/credits HTTP/1.1" 200 OK
2025-09-29T04:14:11.818501223Z INFO:     156.204.156.48:0 - "GET /api/payment/user/credits HTTP/1.1" 200 OK
2025-09-29T04:14:12.016874629Z INFO:     156.204.156.48:0 - "GET /api/payment/user/credits HTTP/1.1" 200 OK
2025-09-29T04:14:12.20268587Z INFO:     156.204.156.48:0 - "GET /api/payment/user/credits HTTP/1.1" 200 OK
2025-09-29T04:14:12.388311376Z INFO:     156.204.156.48:0 - "GET /api/payment/user/credits HTTP/1.1" 200 OK
2025-09-29T04:14:13.493351578Z INFO:     156.204.156.48:0 - "OPTIONS /api/payment/plans HTTP/1.1" 200 OK
2025-09-29T04:14:13.648980902Z INFO:     156.204.156.48:0 - "GET /api/payment/plans HTTP/1.1" 200 OK
2025-09-29T04:14:13.676912374Z WARNING:src.payments.endpoints:🔍 No subscription found for user bpR6MB3823T20EK7BEa3cs2y22u2
2025-09-29T04:14:13.683848476Z WARNING:src.payments.endpoints:User bpR6MB3823T20EK7BEa3cs2y22u2 has no subscription record, returning free tier
2025-09-29T04:14:13.684160665Z INFO:     156.204.156.48:0 - "GET /api/payment/user/subscription HTTP/1.1" 200 OK
2025-09-29T04:14:13.808947992Z INFO:     156.204.156.48:0 - "GET /api/payment/user/credits HTTP/1.1" 200 OK
2025-09-29T04:14:14.086242663Z WARNING:src.payments.endpoints:🔍 No subscription found for user bpR6MB3823T20EK7BEa3cs2y22u2
2025-09-29T04:14:14.091870297Z WARNING:src.payments.endpoints:User bpR6MB3823T20EK7BEa3cs2y22u2 has no subscription record, returning free tier
2025-09-29T04:14:14.092225937Z INFO:     156.204.156.48:0 - "GET /api/payment/user/subscription HTTP/1.1" 200 OK
2025-09-29T04:14:14.200757672Z INFO:     156.204.156.48:0 - "GET /api/payment/user/credits HTTP/1.1" 200 OK
2025-09-29T04:14:25.444805858Z INFO:     156.204.156.48:0 - "OPTIONS /api/payment/checkout HTTP/1.1" 200 OK
2025-09-29T04:14:26.000257644Z WARNING:src.payments.endpoints:🔍 No subscription found for user bpR6MB3823T20EK7BEa3cs2y22u2
2025-09-29T04:14:26.008742741Z WARNING:src.payments.endpoints:User bpR6MB3823T20EK7BEa3cs2y22u2 has no subscription record, returning free tier
2025-09-29T04:14:26.009222235Z 🎯 STEP 1: CREATE_CHECKOUT ENDPOINT CALLED
2025-09-29T04:14:26.009233335Z Request data: variant_id='1013286' success_url='https://www.productgeniepro.com/billing?success=true' cancel_url='https://www.productgeniepro.com/pricing?cancelled=true'
2025-09-29T04:14:26.009238016Z Variant ID: 1013286
2025-09-29T04:14:26.009242376Z Success URL: https://www.productgeniepro.com/billing?success=true
2025-09-29T04:14:26.009246426Z Cancel URL: https://www.productgeniepro.com/pricing?cancelled=true
2025-09-29T04:14:26.009251116Z 🎯 STEP 2: GETTING CLIENT INFO
2025-09-29T04:14:26.009255266Z Client info: {'ip_address': '156.204.156.48', 'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36', 'correlation_id': '5c7d88b1-8799-4035-acd0-fab23c3601ce'}
2025-09-29T04:14:26.009261516Z 🎯 STEP 3: EXTRACTING AUTH DATA
2025-09-29T04:14:26.009265306Z User ID: bpR6MB3823T20EK7BEa3cs2y22u2
2025-09-29T04:14:26.009269126Z User email: ziad321hussein@gmail.com
2025-09-29T04:14:26.009272826Z 🎯 STEP 4: VALIDATING USER
2025-09-29T04:14:26.009276407Z ✅ STEP 4 SUCCESS: User validated
2025-09-29T04:14:26.009280217Z 🎯 STEP 5: VALIDATING VARIANT ID
2025-09-29T04:14:26.009283967Z ✅ STEP 5 SUCCESS: Variant ID validated
2025-09-29T04:14:26.009287987Z 🎯 STEP 6: CALLING LEMON_SQUEEZY SERVICE
2025-09-29T04:14:26.009291777Z 🎯 LEMON SQUEEZY PAYLOAD DEBUG 🎯
2025-09-29T04:14:26.009295637Z === VARIABLES ===
2025-09-29T04:14:26.009299567Z Variant ID: 1013286
2025-09-29T04:14:26.009303307Z Store ID: 224253
2025-09-29T04:14:26.009307127Z User ID: bpR6MB3823T20EK7BEa3cs2y22u2
2025-09-29T04:14:26.009311108Z User Email: ziad321hussein@gmail.com
2025-09-29T04:14:26.009314958Z Success URL: https://www.productgeniepro.com/billing?success=true
2025-09-29T04:14:26.009318818Z Cancel URL: https://www.productgeniepro.com/pricing?cancelled=true
2025-09-29T04:14:26.009336978Z Test Mode: True
2025-09-29T04:14:26.009339608Z === PAYLOAD BEING SENT ===
2025-09-29T04:14:26.009341799Z {
2025-09-29T04:14:26.009344389Z   "data": {
2025-09-29T04:14:26.009346649Z     "type": "checkouts",
2025-09-29T04:14:26.009348929Z     "attributes": {
2025-09-29T04:14:26.009351189Z       "checkout_options": {
2025-09-29T04:14:26.009353369Z         "embed": false,
2025-09-29T04:14:26.009355499Z         "media": false
2025-09-29T04:14:26.009357659Z       },
2025-09-29T04:14:26.009359869Z       "checkout_data": {
2025-09-29T04:14:26.009364169Z         "email": "ziad321hussein@gmail.com",
2025-09-29T04:14:26.009366589Z         "custom": {
2025-09-29T04:14:26.009369269Z           "user_id": "bpR6MB3823T20EK7BEa3cs2y22u2"
2025-09-29T04:14:26.009371489Z         }
2025-09-29T04:14:26.009373549Z       },
2025-09-29T04:14:26.009375929Z       "product_options": {
2025-09-29T04:14:26.00937829Z         "redirect_url": "https://www.productgeniepro.com/billing?success=true"
2025-09-29T04:14:26.00938052Z       }
2025-09-29T04:14:26.00938264Z     },
2025-09-29T04:14:26.00938488Z     "relationships": {
2025-09-29T04:14:26.00938704Z       "store": {
2025-09-29T04:14:26.0093892Z         "data": {
2025-09-29T04:14:26.00939136Z           "type": "stores",
2025-09-29T04:14:26.00939358Z           "id": "224253"
2025-09-29T04:14:26.00939585Z         }
2025-09-29T04:14:26.00939801Z       },
2025-09-29T04:14:26.00940017Z       "variant": {
2025-09-29T04:14:26.00940234Z         "data": {
2025-09-29T04:14:26.00940449Z           "type": "variants",
2025-09-29T04:14:26.00940665Z           "id": "1013286"
2025-09-29T04:14:26.00940891Z         }
2025-09-29T04:14:26.009411061Z       }
2025-09-29T04:14:26.009413251Z     }
2025-09-29T04:14:26.009415371Z   }
2025-09-29T04:14:26.009417621Z }
2025-09-29T04:14:26.009419921Z === HEADERS ===
2025-09-29T04:14:26.009422161Z {
2025-09-29T04:14:26.009425231Z   "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5NGQ1OWNlZi1kYmI4LTRlYTUtYjE3OC1kMjU0MGZjZDY5MTkiLCJqdGkiOiJkOGY2NTljZjdhMzA3ZGNjM2RjNTk4ZjNiMzU4YTk3YTczYzdhNGJkNDg2ZDlkM2JhYTE4OGQ4Y2MxMGU1Zjc5YWQzODJkZTgyYjgxNjRiNiIsImlhdCI6MTc1ODgyNzU5MC41NzYwMjcsIm5iZiI6MTc1ODgyNzU5MC41NzYwMjksImV4cCI6MjA3NDM2MDM5MC41NjA2NzcsInN1YiI6IjU1NzE5NjQiLCJzY29wZXMiOltdfQ.v6DQ8CrPGAovPSiYrv6Y3GkQ3DWHPcC0aAiZ9mP5BsXCwXoz5Kf1OY-fLAHC4ikcmx2RYZuLbSrF_Xxa4mvw2exFnJMsODiiuzItzhdVGUwR89IzbFAD6hcto-w0ERT3gjP781BJ-lxa7pzC4tCADeRhAtMPM7MZ7h7g-0JsRjXyNDrM0ArKoN84kiGHojmPCBomBuXTQ-mC_VQEWn8PKxTbZEem7FoyP4ydK46xYQu-naukuPTOZHRQ44Mdz_16JQ7Cda2pbfJo2osSPGaLTYUKvH0-aF2jlZToxGCPPr8LbPsHo1-96W2D6CBkCF0kFd6BQd0PKw64X-2ywolNwyna51cLKvkZuOHrh2Z8XVG0GONxeo6b1mFzgs8PzSkaPJ5Er_vhcRQVhAolOVmBHcZ61FUUJ208hR1FUVzMHlrTWtcTAi6HUjthHZB2ZL0xrIkDcWQPxG38i8ArAslXFLytqDTU3tePixq0WDHHBnBq8XSbleFoLH8rdc0j4v5KEPoJyXUS7MrHkiJ602WwLFPuczEdkRPvnSNeRKhsSlPkO8SiQFdHZ6VLCGQoEWDvm7SL2U6lmOJ2T1imOAGiTveGoliycICl_HQo29Fk0VFMFVa_jei7HCgdsLArClUHceqfx5UTOsrWxcd8zr75ALBqDzIWT9tpG5ifdTappes",
2025-09-29T04:14:26.009427891Z   "Accept": "application/vnd.api+json",
2025-09-29T04:14:26.009430241Z   "Content-Type": "application/vnd.api+json",
2025-09-29T04:14:26.009432621Z   "Version": "2021-07-07"
2025-09-29T04:14:26.009434751Z }
2025-09-29T04:14:26.009437001Z === API ENDPOINT ===
2025-09-29T04:14:26.009439271Z POST https://api.lemonsqueezy.com/v1/checkouts
2025-09-29T04:14:26.009441922Z INFO:     156.204.156.48:0 - "GET /api/payment/user/subscription HTTP/1.1" 200 OK
2025-09-29T04:14:26.055453049Z === RESPONSE ===
2025-09-29T04:14:26.05547585Z Status: Unknown
2025-09-29T04:14:26.05547854Z Response: {
2025-09-29T04:14:26.0554812Z   "jsonapi": {
2025-09-29T04:14:26.055512781Z     "version": "1.0"
2025-09-29T04:14:26.055515671Z   },
2025-09-29T04:14:26.055518241Z   "links": {
2025-09-29T04:14:26.055520921Z     "self": "https://api.lemonsqueezy.com/v1/checkouts/130d954a-ec3a-42b7-b6af-a72f0c20df1f"
2025-09-29T04:14:26.055523441Z   },
2025-09-29T04:14:26.055525781Z   "data": {
2025-09-29T04:14:26.055528301Z     "type": "checkouts",
2025-09-29T04:14:26.055531061Z     "id": "130d954a-ec3a-42b7-b6af-a72f0c20df1f",
2025-09-29T04:14:26.055533411Z     "attributes": {
2025-09-29T04:14:26.055536202Z       "store_id": 224253,
2025-09-29T04:14:26.055538782Z       "variant_id": 1013286,
2025-09-29T04:14:26.055541262Z       "custom_price": null,
2025-09-29T04:14:26.055543762Z       "product_options": {
2025-09-29T04:14:26.055546282Z         "name": "",
2025-09-29T04:14:26.055548552Z         "description": "",
2025-09-29T04:14:26.055551092Z         "media": [],
2025-09-29T04:14:26.055554052Z         "redirect_url": "https://www.productgeniepro.com/billing?success=true",
2025-09-29T04:14:26.055557102Z         "receipt_button_text": "",
2025-09-29T04:14:26.055559532Z         "receipt_link_url": "",
2025-09-29T04:14:26.055561942Z         "receipt_thank_you_note": "",
2025-09-29T04:14:26.055564352Z         "enabled_variants": [],
2025-09-29T04:14:26.055566792Z         "confirmation_title": "",
2025-09-29T04:14:26.055569232Z         "confirmation_message": "",
2025-09-29T04:14:26.055571792Z         "confirmation_button_text": ""
2025-09-29T04:14:26.055574123Z       },
2025-09-29T04:14:26.055576463Z       "checkout_options": {
2025-09-29T04:14:26.055578803Z         "embed": false,
2025-09-29T04:14:26.055581063Z         "media": false,
2025-09-29T04:14:26.055583503Z         "logo": true,
2025-09-29T04:14:26.055585923Z         "desc": true,
2025-09-29T04:14:26.055588323Z         "discount": true,
2025-09-29T04:14:26.055590833Z         "skip_trial": false,
2025-09-29T04:14:26.055593263Z         "quantity": 1,
2025-09-29T04:14:26.055595993Z         "subscription_preview": true,
2025-09-29T04:14:26.055598613Z         "locale": "en"
2025-09-29T04:14:26.055601073Z       },
2025-09-29T04:14:26.055603453Z       "checkout_data": {
2025-09-29T04:14:26.055605784Z         "email": "ziad321hussein@gmail.com",
2025-09-29T04:14:26.055608284Z         "name": "",
2025-09-29T04:14:26.055610724Z         "billing_address": [],
2025-09-29T04:14:26.055613134Z         "tax_number": "",
2025-09-29T04:14:26.055615464Z         "discount_code": "",
2025-09-29T04:14:26.055618044Z         "custom": {
2025-09-29T04:14:26.055620334Z           "user_id": "bpR6MB3823T20EK7BEa3cs2y22u2"
2025-09-29T04:14:26.055622794Z         },
2025-09-29T04:14:26.055625154Z         "variant_quantities": []
2025-09-29T04:14:26.055627494Z       },
2025-09-29T04:14:26.055629794Z       "preview": false,
2025-09-29T04:14:26.055632104Z       "expires_at": null,
2025-09-29T04:14:26.055634614Z       "created_at": "2025-09-29T04:14:25.000000Z",
2025-09-29T04:14:26.055637094Z       "updated_at": "2025-09-29T04:14:26.000000Z",
2025-09-29T04:14:26.055639554Z       "test_mode": true,
2025-09-29T04:14:26.055642674Z       "url": "https://product-genie.lemonsqueezy.com/checkout/custom/130d954a-ec3a-42b7-b6af-a72f0c20df1f?signature=2e5e6176eb51b354a6254f964b0624e8211a8cdd505a0df2ff4fd4fcd6380933"
2025-09-29T04:14:26.055645235Z     },
2025-09-29T04:14:26.055647615Z     "relationships": {
2025-09-29T04:14:26.055738987Z       "store": {
2025-09-29T04:14:26.055746577Z         "links": {
2025-09-29T04:14:26.055749758Z           "related": "https://api.lemonsqueezy.com/v1/checkouts/130d954a-ec3a-42b7-b6af-a72f0c20df1f/store",
2025-09-29T04:14:26.055759528Z           "self": "https://api.lemonsqueezy.com/v1/checkouts/130d954a-ec3a-42b7-b6af-a72f0c20df1f/relationships/store"
2025-09-29T04:14:26.055762078Z         }
2025-09-29T04:14:26.055764588Z       },
2025-09-29T04:14:26.055766918Z       "variant": {
2025-09-29T04:14:26.055769238Z         "links": {
2025-09-29T04:14:26.055771698Z           "related": "https://api.lemonsqueezy.com/v1/checkouts/130d954a-ec3a-42b7-b6af-a72f0c20df1f/variant",
2025-09-29T04:14:26.055774078Z           "self": "https://api.lemonsqueezy.com/v1/checkouts/130d954a-ec3a-42b7-b6af-a72f0c20df1f/relationships/variant"
2025-09-29T04:14:26.055776378Z         }
2025-09-29T04:14:26.055778689Z       }
2025-09-29T04:14:26.055780898Z     },
2025-09-29T04:14:26.055783119Z     "links": {
2025-09-29T04:14:26.055785699Z       "self": "https://api.lemonsqueezy.com/v1/checkouts/130d954a-ec3a-42b7-b6af-a72f0c20df1f"
2025-09-29T04:14:26.055787929Z     }
2025-09-29T04:14:26.055790239Z   }
2025-09-29T04:14:26.055792469Z }
2025-09-29T04:14:26.055794929Z ✅ STEP 6 SUCCESS: Lemon Squeezy service call successful
2025-09-29T04:14:26.055798209Z Result: {'success': True, 'checkout_url': 'https://product-genie.lemonsqueezy.com/checkout/custom/130d954a-ec3a-42b7-b6af-a72f0c20df1f?signature=2e5e6176eb51b354a6254f964b0624e8211a8cdd505a0df2ff4fd4fcd6380933', 'checkout_id': '130d954a-ec3a-42b7-b6af-a72f0c20df1f'}
2025-09-29T04:14:26.055800599Z INFO:     156.204.156.48:0 - "POST /api/payment/checkout HTTP/1.1" 200 OK
2025-09-29T04:14:26.094583786Z INFO:     156.204.156.48:0 - "GET /api/payment/user/credits HTTP/1.1" 200 OK
2025-09-29T04:14:28.46213854Z INFO:     connection closed
2025-09-29T04:15:06.321600216Z WARNING:security:{"event_type": "webhook_received", "user_id": null, "timestamp": "2025-09-29T04:15:06.321339+00:00", "ip_address": null, "user_agent": null, "event_data": {"signature_provided": true, "signature_valid": true}, "security_level": "high", "success": true, "error_message": null, "session_id": null, "correlation_id": null}
2025-09-29T04:15:06.377401328Z 🎯 WEBHOOK RECEIVED: POST https://ai-product-descriptions.onrender.com/api/payment/webhook
2025-09-29T04:15:06.377434089Z 🎯 WEBHOOK HEADERS: {'host': 'ai-product-descriptions.onrender.com', 'user-agent': 'LemonSqueezy-Hookshot', 'content-length': '1997', 'accept-encoding': 'gzip, br', 'cdn-loop': 'cloudflare; loops=1', 'cf-connecting-ip': '18.116.135.47', 'cf-ipcountry': 'US', 'cf-ray': '9868a8503a58eee6-CMH', 'cf-visitor': '{"scheme":"https"}', 'content-type': 'application/json', 'render-proxy-ttl': '4', 'rndr-id': '8a381f7a-a9d2-4161', 'true-client-ip': '18.116.135.47', 'x-event-name': 'subscription_payment_success', 'x-forwarded-for': '18.116.135.47, 104.23.243.80, 10.226.151.1', 'x-forwarded-proto': 'https', 'x-request-start': '1759119306317094', 'x-signature': '8cbe1c17067003f52d88284f735000808eeb16ad2f72dbe5f62cae4b3680a809'}
2025-09-29T04:15:06.377441539Z 🎯 BillingService: Processing webhook event_id=8cbe1c17067003f52d88284f735000808eeb16ad2f72dbe5f62cae4b3680a809
2025-09-29T04:15:06.377446639Z 🎯 BillingService: Event data: {'meta': {'test_mode': True, 'event_name': 'subscription_payment_success', 'custom_data': {'user_id': 'bpR6MB3823T20EK7BEa3cs2y22u2'}, 'webhook_id': '6a835014-b8ea-4bf5-910b-8773edf6d5d0'}, 'data': {'type': 'subscription-invoices', 'id': '4591918', 'attributes': {'store_id': 224253, 'subscription_id': 1522295, 'customer_id': 6829303, 'user_name': 'Zeyad Sherif', 'user_email': 'ziad321hussein@gmail.com', 'billing_reason': 'initial', 'card_brand': 'visa', 'card_last_four': '4242', 'currency': 'USD', 'currency_rate': '1.00000000', 'status': 'paid', 'status_formatted': 'Paid', 'refunded': False, 'refunded_at': None, 'subtotal': 499, 'discount_total': 0, 'tax': 0, 'tax_inclusive': False, 'total': 499, 'refunded_amount': 0, 'subtotal_usd': 499, 'discount_total_usd': 0, 'tax_usd': 0, 'total_usd': 499, 'refunded_amount_usd': 0, 'subtotal_formatted': '$4.99', 'discount_total_formatted': '$0.00', 'tax_formatted': '$0.00', 'total_formatted': '$4.99', 'refunded_amount_formatted': '$0.00', 'urls': {'invoice_url': 'https://app.lemonsqueezy.com/my-orders/3a557475-ba96-4030-a02e-03fa4d430de5/subscription-invoice/4591918?expires=1759140906&signature=6893d7b4c15653f828934b1636e1a5f8d322bf0e5b667b4373eeacbe2805e242'}, 'created_at': '2025-09-29T04:15:01.000000Z', 'updated_at': '2025-09-29T04:15:06.000000Z', 'test_mode': True}, 'relationships': {'store': {'links': {'related': 'https://api.lemonsqueezy.com/v1/subscription-invoices/4591918/store', 'self': 'https://api.lemonsqueezy.com/v1/subscription-invoices/4591918/relationships/store'}}, 'subscription': {'links': {'related': 'https://api.lemonsqueezy.com/v1/subscription-invoices/4591918/subscription', 'self': 'https://api.lemonsqueezy.com/v1/subscription-invoices/4591918/relationships/subscription'}}, 'customer': {'links': {'related': 'https://api.lemonsqueezy.com/v1/subscription-invoices/4591918/customer', 'self': 'https://api.lemonsqueezy.com/v1/subscription-invoices/4591918/relationships/customer'}}}, 'links': {'self': 'https://api.lemonsqueezy.com/v1/subscription-invoices/4591918'}}}
2025-09-29T04:15:06.377464369Z 🎯 BillingService: Event 8cbe1c17067003f52d88284f735000808eeb16ad2f72dbe5f62cae4b3680a809 is new, processing...
2025-09-29T04:15:06.37746846Z 🎯 BillingService: Event type: subscription_payment_success
2025-09-29T04:15:06.37747705Z 🎯 BillingService: Attributes: {'store_id': 224253, 'subscription_id': 1522295, 'customer_id': 6829303, 'user_name': 'Zeyad Sherif', 'user_email': 'ziad321hussein@gmail.com', 'billing_reason': 'initial', 'card_brand': 'visa', 'card_last_four': '4242', 'currency': 'USD', 'currency_rate': '1.00000000', 'status': 'paid', 'status_formatted': 'Paid', 'refunded': False, 'refunded_at': None, 'subtotal': 499, 'discount_total': 0, 'tax': 0, 'tax_inclusive': False, 'total': 499, 'refunded_amount': 0, 'subtotal_usd': 499, 'discount_total_usd': 0, 'tax_usd': 0, 'total_usd': 499, 'refunded_amount_usd': 0, 'subtotal_formatted': '$4.99', 'discount_total_formatted': '$0.00', 'tax_formatted': '$0.00', 'total_formatted': '$4.99', 'refunded_amount_formatted': '$0.00', 'urls': {'invoice_url': 'https://app.lemonsqueezy.com/my-orders/3a557475-ba96-4030-a02e-03fa4d430de5/subscription-invoice/4591918?expires=1759140906&signature=6893d7b4c15653f828934b1636e1a5f8d322bf0e5b667b4373eeacbe2805e242'}, 'created_at': '2025-09-29T04:15:01.000000Z', 'updated_at': '2025-09-29T04:15:06.000000Z', 'test_mode': True}
2025-09-29T04:15:06.37748205Z ✅ Using user_id: bpR6MB3823T20EK7BEa3cs2y22u2
2025-09-29T04:15:06.37748593Z 🎯 BillingService: Checking event type 'subscription_payment_success' against subscription events
2025-09-29T04:15:06.37749007Z 🎯 BillingService: is_subscription_event=True, has_subscription_data=False
2025-09-29T04:15:06.37749277Z 🎯 Processing payment success event for user bpR6MB3823T20EK7BEa3cs2y22u2
2025-09-29T04:15:06.377497541Z 🔧 Payment success: Using existing plan pro
2025-09-29T04:15:06.377500001Z ✅ Ensured user bpR6MB3823T20EK7BEa3cs2y22u2 exists in users table
2025-09-29T04:15:06.377502711Z 🔄 Updating existing subscription for user bpR6MB3823T20EK7BEa3cs2y22u2: pro -> pro
2025-09-29T04:15:06.377505261Z ✅ Updated subscription for user bpR6MB3823T20EK7BEa3cs2y22u2: plan=pro, status=SubscriptionStatus.active
2025-09-29T04:15:06.377507871Z ✅ Updated Subscription table for user bpR6MB3823T20EK7BEa3cs2y22u2: plan=pro
2025-09-29T04:15:06.377510811Z ✅ Created new UserSubscription for user bpR6MB3823T20EK7BEa3cs2y22u2: plan_id=pro
2025-09-29T04:15:06.377513181Z ✅ Updated subscription for user bpR6MB3823T20EK7BEa3cs2y22u2: plan=pro, status=active
2025-09-29T04:15:06.377522031Z INFO:     18.116.135.47:0 - "POST /api/payment/webhook HTTP/1.1" 200 OK
2025-09-29T04:15:07.250172971Z WARNING:security:{"event_type": "webhook_received", "user_id": null, "timestamp": "2025-09-29T04:15:07.249898+00:00", "ip_address": null, "user_agent": null, "event_data": {"signature_provided": true, "signature_valid": true}, "security_level": "high", "success": true, "error_message": null, "session_id": null, "correlation_id": null}
2025-09-29T04:15:07.275064014Z 🎯 WEBHOOK RECEIVED: POST https://ai-product-descriptions.onrender.com/api/payment/webhook
2025-09-29T04:15:07.275081164Z 🎯 WEBHOOK HEADERS: {'host': 'ai-product-descriptions.onrender.com', 'user-agent': 'LemonSqueezy-Hookshot', 'content-length': '3394', 'accept-encoding': 'gzip, br', 'cdn-loop': 'cloudflare; loops=1', 'cf-connecting-ip': '18.116.135.47', 'cf-ipcountry': 'US', 'cf-ray': '9868a8563ead97b7-CMH', 'cf-visitor': '{"scheme":"https"}', 'content-type': 'application/json', 'render-proxy-ttl': '4', 'rndr-id': '4138448c-6aa7-4b90', 'true-client-ip': '18.116.135.47', 'x-event-name': 'subscription_created', 'x-forwarded-for': '18.116.135.47, 104.23.243.80, 10.226.151.1', 'x-forwarded-proto': 'https', 'x-request-start': '1759119307246711', 'x-signature': 'fe0170b4c48da0454d25a808bacc3114303d4c0ce6f9d587eb4d3f22eccaf8a3'}
2025-09-29T04:15:07.275085105Z 🎯 BillingService: Processing webhook event_id=fe0170b4c48da0454d25a808bacc3114303d4c0ce6f9d587eb4d3f22eccaf8a3
2025-09-29T04:15:07.275091135Z 🎯 BillingService: Event data: {'meta': {'test_mode': True, 'event_name': 'subscription_created', 'custom_data': {'user_id': 'bpR6MB3823T20EK7BEa3cs2y22u2'}, 'webhook_id': 'fa35a15c-3830-4cd6-9f02-161945e69243'}, 'data': {'type': 'subscriptions', 'id': '1522295', 'attributes': {'store_id': 224253, 'customer_id': 6829303, 'order_id': 6495556, 'order_item_id': 6439379, 'product_id': 645534, 'variant_id': 1013286, 'product_name': 'Get Extra Product Descriptions', 'variant_name': 'Pro Plan', 'user_name': 'Zeyad Sherif', 'user_email': 'ziad321hussein@gmail.com', 'status': 'active', 'status_formatted': 'Active', 'card_brand': 'visa', 'card_last_four': '4242', 'payment_processor': 'stripe', 'pause': None, 'cancelled': False, 'trial_ends_at': None, 'billing_anchor': 29, 'first_subscription_item': {'id': 4541497, 'subscription_id': 1522295, 'price_id': 1608947, 'quantity': 1, 'is_usage_based': False, 'created_at': '2025-09-29T04:15:07.000000Z', 'updated_at': '2025-09-29T04:15:07.000000Z'}, 'urls': {'update_payment_method': 'https://product-genie.lemonsqueezy.com/subscription/1522295/payment-details?expires=1759140907&signature=8de0f871b53351f996dace28152055ef350a90000e3ec7a14285701d9cb8f801', 'customer_portal': 'https://product-genie.lemonsqueezy.com/billing?expires=1759140907&test_mode=1&user=5534177&signature=2cff4bbcda0adfef291bd8ea5e635e54a88c1caf8f22b0ad8cb030eb78ec0a5e', 'customer_portal_update_subscription': 'https://product-genie.lemonsqueezy.com/billing/1522295/update?expires=1759140907&user=5534177&signature=5bb2562959a0de947a16270f918082fe6024bb206450c9c0bf055353648b6ede'}, 'renews_at': '2025-10-29T04:14:56.000000Z', 'ends_at': None, 'created_at': '2025-09-29T04:14:58.000000Z', 'updated_at': '2025-09-29T04:15:04.000000Z', 'test_mode': True}, 'relationships': {'store': {'links': {'related': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/store', 'self': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/relationships/store'}}, 'customer': {'links': {'related': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/customer', 'self': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/relationships/customer'}}, 'order': {'links': {'related': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/order', 'self': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/relationships/order'}}, 'order-item': {'links': {'related': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/order-item', 'self': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/relationships/order-item'}}, 'product': {'links': {'related': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/product', 'self': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/relationships/product'}}, 'variant': {'links': {'related': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/variant', 'self': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/relationships/variant'}}, 'subscription-items': {'links': {'related': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/subscription-items', 'self': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/relationships/subscription-items'}}, 'subscription-invoices': {'links': {'related': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/subscription-invoices', 'self': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/relationships/subscription-invoices'}}}, 'links': {'self': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295'}}}
2025-09-29T04:15:07.275106845Z 🎯 BillingService: Event fe0170b4c48da0454d25a808bacc3114303d4c0ce6f9d587eb4d3f22eccaf8a3 is new, processing...
2025-09-29T04:15:07.275110125Z 🎯 BillingService: Event type: subscription_created
2025-09-29T04:15:07.275126776Z 🎯 BillingService: Attributes: {'store_id': 224253, 'customer_id': 6829303, 'order_id': 6495556, 'order_item_id': 6439379, 'product_id': 645534, 'variant_id': 1013286, 'product_name': 'Get Extra Product Descriptions', 'variant_name': 'Pro Plan', 'user_name': 'Zeyad Sherif', 'user_email': 'ziad321hussein@gmail.com', 'status': 'active', 'status_formatted': 'Active', 'card_brand': 'visa', 'card_last_four': '4242', 'payment_processor': 'stripe', 'pause': None, 'cancelled': False, 'trial_ends_at': None, 'billing_anchor': 29, 'first_subscription_item': {'id': 4541497, 'subscription_id': 1522295, 'price_id': 1608947, 'quantity': 1, 'is_usage_based': False, 'created_at': '2025-09-29T04:15:07.000000Z', 'updated_at': '2025-09-29T04:15:07.000000Z'}, 'urls': {'update_payment_method': 'https://product-genie.lemonsqueezy.com/subscription/1522295/payment-details?expires=1759140907&signature=8de0f871b53351f996dace28152055ef350a90000e3ec7a14285701d9cb8f801', 'customer_portal': 'https://product-genie.lemonsqueezy.com/billing?expires=1759140907&test_mode=1&user=5534177&signature=2cff4bbcda0adfef291bd8ea5e635e54a88c1caf8f22b0ad8cb030eb78ec0a5e', 'customer_portal_update_subscription': 'https://product-genie.lemonsqueezy.com/billing/1522295/update?expires=1759140907&user=5534177&signature=5bb2562959a0de947a16270f918082fe6024bb206450c9c0bf055353648b6ede'}, 'renews_at': '2025-10-29T04:14:56.000000Z', 'ends_at': None, 'created_at': '2025-09-29T04:14:58.000000Z', 'updated_at': '2025-09-29T04:15:04.000000Z', 'test_mode': True}
2025-09-29T04:15:07.275135176Z ✅ Using user_id: bpR6MB3823T20EK7BEa3cs2y22u2
2025-09-29T04:15:07.275138416Z 🎯 BillingService: Checking event type 'subscription_created' against subscription events
2025-09-29T04:15:07.275141326Z 🎯 BillingService: is_subscription_event=True, has_subscription_data=True
2025-09-29T04:15:07.275144086Z 🔧 Mapping variant_id: 1013286 (type: <class 'int'>)
2025-09-29T04:15:07.275146446Z 🔧 Available mappings: {'1013286': 'pro', '1013276': 'enterprise', '1013282': 'pro-yearly'}
2025-09-29T04:15:07.275149437Z 🔧 Mapped to plan: pro
2025-09-29T04:15:07.275151746Z 🔧 Mapped variant_id 1013286 to plan: pro
2025-09-29T04:15:07.275154177Z ✅ Ensured user bpR6MB3823T20EK7BEa3cs2y22u2 exists in users table
2025-09-29T04:15:07.275156557Z 🔄 Updating existing subscription for user bpR6MB3823T20EK7BEa3cs2y22u2: pro -> pro
2025-09-29T04:15:07.275159237Z ✅ Updated subscription for user bpR6MB3823T20EK7BEa3cs2y22u2: plan=pro, status=SubscriptionStatus.active
2025-09-29T04:15:07.275161487Z ✅ Updated Subscription table for user bpR6MB3823T20EK7BEa3cs2y22u2: plan=pro
2025-09-29T04:15:07.275163927Z ✅ Updated UserSubscription table for user bpR6MB3823T20EK7BEa3cs2y22u2: plan_id=pro, status=active
2025-09-29T04:15:07.275174637Z ✅ Updated subscription for user bpR6MB3823T20EK7BEa3cs2y22u2: plan=pro, status=SubscriptionStatus.active
2025-09-29T04:15:07.275177297Z ✅ Committed subscription update to database
2025-09-29T04:15:07.275179767Z INFO:     18.116.135.47:0 - "POST /api/payment/webhook HTTP/1.1" 200 OK
2025-09-29T04:15:09.578383215Z INFO:     156.204.156.48:0 - "WebSocket /ws/payments" [accepted]
2025-09-29T04:15:09.578590731Z INFO:     connection open
2025-09-29T04:15:09.742653191Z INFO:     156.204.156.48:0 - "GET /api/payment/user/credits HTTP/1.1" 200 OK
2025-09-29T04:15:09.890664474Z INFO:     156.204.156.48:0 - "GET /api/payment/user/subscription HTTP/1.1" 200 OK
2025-09-29T04:15:10.045372791Z INFO:     156.204.156.48:0 - "GET /api/payment/user/subscription HTTP/1.1" 200 OK
2025-09-29T04:15:10.098547267Z INFO:     156.204.156.48:0 - "GET /api/payment/user/credits HTTP/1.1" 200 OK
2025-09-29T04:15:10.229511225Z INFO:     156.204.156.48:0 - "GET /api/payment/user/subscription HTTP/1.1" 200 OK
2025-09-29T04:15:10.284645807Z INFO:     156.204.156.48:0 - "GET /api/payment/user/credits HTTP/1.1" 200 OK
2025-09-29T04:15:10.479249905Z INFO:     156.204.156.48:0 - "GET /api/payment/user/credits HTTP/1.1" 200 OK
2025-09-29T04:15:10.686807619Z INFO:     156.204.156.48:0 - "GET /api/payment/user/credits HTTP/1.1" 200 OK
2025-09-29T04:15:14.091659494Z INFO:     156.204.156.48:0 - "GET /api/payment/plans HTTP/1.1" 200 OK
2025-09-29T04:15:14.298221799Z INFO:     156.204.156.48:0 - "GET /api/payment/user/subscription HTTP/1.1" 200 OK
2025-09-29T04:15:14.358239444Z INFO:     156.204.156.48:0 - "GET /api/payment/user/credits HTTP/1.1" 200 OK
2025-09-29T04:15:14.656029441Z INFO:     156.204.156.48:0 - "GET /api/payment/user/subscription HTTP/1.1" 200 OK
2025-09-29T04:15:14.771635092Z INFO:     156.204.156.48:0 - "GET /api/payment/user/credits HTTP/1.1" 200 OK
2025-09-29T04:15:14.844247543Z INFO:     156.204.156.48:0 - "GET /api/payment/user/subscription HTTP/1.1" 200 OK
2025-09-29T04:15:14.932468488Z INFO:     156.204.156.48:0 - "GET /api/payment/user/credits HTTP/1.1" 200 OK
2025-09-29T04:15:19.194187024Z INFO:     156.204.156.48:0 - "GET /api/payment/user/subscription HTTP/1.1" 200 OK
2025-09-29T04:15:19.272617984Z INFO:     156.204.156.48:0 - "GET /api/payment/user/credits HTTP/1.1" 200 OK
2025-09-29T04:15:19.58619064Z INFO:     156.204.156.48:0 - "GET /api/payment/user/subscription HTTP/1.1" 200 OK
2025-09-29T04:15:19.684111787Z INFO:     156.204.156.48:0 - "GET /api/payment/user/credits HTTP/1.1" 200 OK
2025-09-29T04:15:19.818387001Z INFO:     156.204.156.48:0 - "GET /api/payment/user/subscription HTTP/1.1" 200 OK
2025-09-29T04:15:19.968737042Z INFO:     156.204.156.48:0 - "GET /api/payment/user/credits HTTP/1.1" 200 OK
2025-09-29T04:15:35.331103923Z WARNING:security:{"event_type": "webhook_received", "user_id": null, "timestamp": "2025-09-29T04:15:35.330905+00:00", "ip_address": null, "user_agent": null, "event_data": {"signature_provided": true, "signature_valid": true}, "security_level": "high", "success": true, "error_message": null, "session_id": null, "correlation_id": null}
2025-09-29T04:15:35.379344515Z 🎯 WEBHOOK RECEIVED: POST https://ai-product-descriptions.onrender.com/api/payment/webhook
2025-09-29T04:15:35.379363926Z 🎯 WEBHOOK HEADERS: {'host': 'ai-product-descriptions.onrender.com', 'user-agent': 'LemonSqueezy-Hookshot', 'content-length': '3394', 'accept-encoding': 'gzip, br', 'cdn-loop': 'cloudflare; loops=1', 'cf-connecting-ip': '18.116.135.47', 'cf-ipcountry': 'US', 'cf-ray': '9868a905bc3e452a-CMH', 'cf-visitor': '{"scheme":"https"}', 'content-type': 'application/json', 'render-proxy-ttl': '4', 'rndr-id': 'df8a7819-e790-4a33', 'true-client-ip': '18.116.135.47', 'x-event-name': 'subscription_updated', 'x-forwarded-for': '18.116.135.47, 104.23.243.80, 10.226.151.1', 'x-forwarded-proto': 'https', 'x-request-start': '1759119335327623', 'x-signature': '2bb63bb3728d12ee63dea0bc7ff55f4318a6920bd9b60785474b13ffff383ecc'}
2025-09-29T04:15:35.379380876Z 🎯 BillingService: Processing webhook event_id=2bb63bb3728d12ee63dea0bc7ff55f4318a6920bd9b60785474b13ffff383ecc
2025-09-29T04:15:35.379396307Z 🎯 BillingService: Event data: {'meta': {'test_mode': True, 'event_name': 'subscription_updated', 'custom_data': {'user_id': 'bpR6MB3823T20EK7BEa3cs2y22u2'}, 'webhook_id': 'd254bf1b-4b43-4312-a457-8d35354364fe'}, 'data': {'type': 'subscriptions', 'id': '1522295', 'attributes': {'store_id': 224253, 'customer_id': 6829303, 'order_id': 6495556, 'order_item_id': 6439379, 'product_id': 645534, 'variant_id': 1013286, 'product_name': 'Get Extra Product Descriptions', 'variant_name': 'Pro Plan', 'user_name': 'Zeyad Sherif', 'user_email': 'ziad321hussein@gmail.com', 'status': 'active', 'status_formatted': 'Active', 'card_brand': 'visa', 'card_last_four': '4242', 'payment_processor': 'stripe', 'pause': None, 'cancelled': False, 'trial_ends_at': None, 'billing_anchor': 29, 'first_subscription_item': {'id': 4541497, 'subscription_id': 1522295, 'price_id': 1608947, 'quantity': 1, 'is_usage_based': False, 'created_at': '2025-09-29T04:15:07.000000Z', 'updated_at': '2025-09-29T04:15:35.000000Z'}, 'urls': {'update_payment_method': 'https://product-genie.lemonsqueezy.com/subscription/1522295/payment-details?expires=1759140935&signature=b03412fd59d8c6d4e0b71246cc7dbc17e5b36e017f4b31380047677fd73cf2a4', 'customer_portal': 'https://product-genie.lemonsqueezy.com/billing?expires=1759140935&test_mode=1&user=5534177&signature=8f02f109e57d59af2348082f0fb66baa242ce4f496def057ba48b160187e1387', 'customer_portal_update_subscription': 'https://product-genie.lemonsqueezy.com/billing/1522295/update?expires=1759140935&user=5534177&signature=f3d744abdee6ea15acc40a9c12c7afa113749f81e5636f572e35f34f4880c9b6'}, 'renews_at': '2025-10-29T04:14:56.000000Z', 'ends_at': None, 'created_at': '2025-09-29T04:14:58.000000Z', 'updated_at': '2025-09-29T04:15:04.000000Z', 'test_mode': True}, 'relationships': {'store': {'links': {'related': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/store', 'self': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/relationships/store'}}, 'customer': {'links': {'related': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/customer', 'self': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/relationships/customer'}}, 'order': {'links': {'related': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/order', 'self': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/relationships/order'}}, 'order-item': {'links': {'related': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/order-item', 'self': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/relationships/order-item'}}, 'product': {'links': {'related': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/product', 'self': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/relationships/product'}}, 'variant': {'links': {'related': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/variant', 'self': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/relationships/variant'}}, 'subscription-items': {'links': {'related': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/subscription-items', 'self': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/relationships/subscription-items'}}, 'subscription-invoices': {'links': {'related': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/subscription-invoices', 'self': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295/relationships/subscription-invoices'}}}, 'links': {'self': 'https://api.lemonsqueezy.com/v1/subscriptions/1522295'}}}
2025-09-29T04:15:35.379400357Z 🎯 BillingService: Event 2bb63bb3728d12ee63dea0bc7ff55f4318a6920bd9b60785474b13ffff383ecc is new, processing...
2025-09-29T04:15:35.379403897Z 🎯 BillingService: Event type: subscription_updated
2025-09-29T04:15:35.379417478Z 🎯 BillingService: Attributes: {'store_id': 224253, 'customer_id': 6829303, 'order_id': 6495556, 'order_item_id': 6439379, 'product_id': 645534, 'variant_id': 1013286, 'product_name': 'Get Extra Product Descriptions', 'variant_name': 'Pro Plan', 'user_name': 'Zeyad Sherif', 'user_email': 'ziad321hussein@gmail.com', 'status': 'active', 'status_formatted': 'Active', 'card_brand': 'visa', 'card_last_four': '4242', 'payment_processor': 'stripe', 'pause': None, 'cancelled': False, 'trial_ends_at': None, 'billing_anchor': 29, 'first_subscription_item': {'id': 4541497, 'subscription_id': 1522295, 'price_id': 1608947, 'quantity': 1, 'is_usage_based': False, 'created_at': '2025-09-29T04:15:07.000000Z', 'updated_at': '2025-09-29T04:15:35.000000Z'}, 'urls': {'update_payment_method': 'https://product-genie.lemonsqueezy.com/subscription/1522295/payment-details?expires=1759140935&signature=b03412fd59d8c6d4e0b71246cc7dbc17e5b36e017f4b31380047677fd73cf2a4', 'customer_portal': 'https://product-genie.lemonsqueezy.com/billing?expires=1759140935&test_mode=1&user=5534177&signature=8f02f109e57d59af2348082f0fb66baa242ce4f496def057ba48b160187e1387', 'customer_portal_update_subscription': 'https://product-genie.lemonsqueezy.com/billing/1522295/update?expires=1759140935&user=5534177&signature=f3d744abdee6ea15acc40a9c12c7afa113749f81e5636f572e35f34f4880c9b6'}, 'renews_at': '2025-10-29T04:14:56.000000Z', 'ends_at': None, 'created_at': '2025-09-29T04:14:58.000000Z', 'updated_at': '2025-09-29T04:15:04.000000Z', 'test_mode': True}
2025-09-29T04:15:35.379427418Z ✅ Using user_id: bpR6MB3823T20EK7BEa3cs2y22u2
2025-09-29T04:15:35.379429488Z 🎯 BillingService: Checking event type 'subscription_updated' against subscription events
2025-09-29T04:15:35.379431548Z 🎯 BillingService: is_subscription_event=True, has_subscription_data=True
2025-09-29T04:15:35.379433198Z 🔧 Mapping variant_id: 1013286 (type: <class 'int'>)
2025-09-29T04:15:35.379434848Z 🔧 Available mappings: {'1013286': 'pro', '1013276': 'enterprise', '1013282': 'pro-yearly'}
2025-09-29T04:15:35.379436828Z 🔧 Mapped to plan: pro
2025-09-29T04:15:35.379438558Z 🔧 Mapped variant_id 1013286 to plan: pro
2025-09-29T04:15:35.379440258Z ✅ Ensured user bpR6MB3823T20EK7BEa3cs2y22u2 exists in users table
2025-09-29T04:15:35.379441978Z 🔄 Updating existing subscription for user bpR6MB3823T20EK7BEa3cs2y22u2: pro -> pro
2025-09-29T04:15:35.379444148Z ✅ Updated subscription for user bpR6MB3823T20EK7BEa3cs2y22u2: plan=pro, status=SubscriptionStatus.active
2025-09-29T04:15:35.379445809Z ✅ Updated Subscription table for user bpR6MB3823T20EK7BEa3cs2y22u2: plan=pro
2025-09-29T04:15:35.379447449Z ✅ Updated UserSubscription table for user bpR6MB3823T20EK7BEa3cs2y22u2: plan_id=pro, status=active
2025-09-29T04:15:35.379449109Z ✅ Updated subscription for user bpR6MB3823T20EK7BEa3cs2y22u2: plan=pro, status=SubscriptionStatus.active
2025-09-29T04:15:35.379450749Z ✅ Committed subscription update to database
2025-09-29T04:15:35.379452399Z INFO:     18.116.135.47:0 - "POST /api/payment/webhook HTTP/1.1" 200 OK