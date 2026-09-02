from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
  return jsonify(
      {"status": "online", "message": "Online Inspectors Backend Active"}
  )


@app.route("/inspect", methods=["GET"])
def inspect_domain():
  domain = request.args.get("domain")
  if not domain:
    return jsonify({"error": "Missing domain parameter"}), 400

  results = {"domain": domain, "rdap": None, "dns": None}

  # 1. Zero-Key RDAP Lookup (Domain Age / Registration Info)
  try:
    rdap_url = f"https://rdap.org/domain/{domain}"
    rdap_response = requests.get(rdap_url, timeout=5)
    if rdap_response.status_code == 200:
      data = rdap_response.json()
      # Extract registration/creation event if available
      events = data.get("events", [])
      creation_date = "Unknown"
      for event in events:
        if event.get("eventAction") == "registration":
          creation_date = event.get("eventDate")
          break
      results["rdap"] = {
          "status": "success",
          "creation_date": creation_date,
          "handle": data.get("handle"),
      }
    else:
      results["rdap"] = {
          "status": "not_found",
          "http_code": rdap_response.status_code,
      }
  except Exception as e:
    results["rdap"] = {"status": "error", "message": str(e)}

  # 2. Zero-Key Google DoH Lookup (DNS Status)
  try:
    dns_url = f"https://dns.google/resolve?name={domain}&type=A"
    dns_response = requests.get(dns_url, timeout=5)
    if dns_response.status_code == 200:
      dns_data = dns_response.json()
      results["dns"] = {
          "status": "success",
          "answers": dns_data.get("Answer", []),
      }
    else:
      results["dns"] = {"status": "failed", "http_code": dns_response.status_code}
  except Exception as e:
    results["dns"] = {"status": "error", "message": str(e)}

  return jsonify(results)


if __name__ == "__main__":
  app.run(debug=True, port=5000)