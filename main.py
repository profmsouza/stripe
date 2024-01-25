from fastapi import FastAPI
import stripe

stripe.api_key = SK_TEST_KEY

app = FastAPI()

@app.get("/")
async def hello():
  return {"Welcome": "iSell payment API is online"}

@app.get("/checkout")
async def checkout(success_url: str, price_id: str):
    cs = stripe.checkout.Session.create(
      success_url=success_url,
      line_items=[{"price": price_id, "quantity": 1}],
      mode="subscription",
    )
    return {"checkout_id": cs.id, "checkout_link": cs.url}
#http://127.0.0.1:8000/checkout?price_id=price_1Oc7QrDSKSSaBlD0kqjAARHS&success_url=https://app.isell.vip/stripe-test?checkout_id={CHECKOUT_SESSION_ID}

@app.get("/identification")
async def identification(checkout_id: str):
    ret_cs=stripe.checkout.Session.retrieve(checkout_id)
    customer_id = ret_cs.customer
    invoice_id = ret_cs.invoice
    payment_id = ret_cs.payment_method_configuration_details.id
    subscription_id = ret_cs.subscription
    return {"checkout_id": checkout_id, "customer_id": customer_id, "invoice_id": invoice_id, "payment_id": payment_id, "subscription_id": subscription_id}
#http://127.0.0.1:8000/identification?checkout_id=cs_test_a1a308PcYgupgAmvcRXCpyJAERjCt5BGWUhlOlv9fnXtInPiYQu6dAFsW2

@app.get("/status")
async def status(sub_id: str):
    sub = stripe.Subscription.retrieve(sub_id)
    return {"status": sub.status}
#http://127.0.0.1:8000/status?sub_id=sub_1OcSGnDSKSSaBlD0OxYHfWjH
