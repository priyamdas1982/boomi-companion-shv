#!/usr/bin/env python3
"""Static design checks for PUB-GB-CG-043 against the SHV build rules (CLAUDE.md) and the design doc.

Pulls the current platform version of every component with the boomi-integration CLI, then asserts
on the XML. Run from the workspace root:

    python3 tests/PUB-GB-CG-043/static_checks.py <skill-path>
"""
import os
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

PROCESS_ID = "1b208fa6-9aa8-4014-b77d-51be59717e91"
PROFILE_ID = "3c0e1d39-0184-4f43-874e-bd7f953b60d1"
WSS_OP_ID = "c54a0d5e-9786-40aa-97d7-8b6c53247526"
KAFKA_OP_ID = "0dea7d10-f8a0-4928-88f8-ee1dfcea1b51"
API_ID = "bd886149-18b9-4900-9376-bb9c05b741b6"
KAFKA_CONN_ID = "c85b494e-58ab-4591-b946-76a9ec636414"
FACADE_ID = "338df4f8-af86-44f9-855c-943d8d0d478f"
FOLDER = ("SHV Energy N.V./01-Sandbox/01-Users/Priyam/BC/GB-CG/Enterprise Projects/"
          "Customer Portal/Publisher/PUB-GB-CG-043-leads")
PROCESS_NAME = "[Publisher]-[PUB-GB-CG-043]-[CreateLead]-[Customer Portal]-[GB-CG]"
TOPIC = "gb-cg.q.leads.in.insert"
PROFILE_FIELDS = ["first-name", "last-name", "phone", "email", "postcode", "address-line-one",
                  "addional-comments", "form-source", "lead-channel", "lead-source"]

results = []


def check(tc, desc, ok, detail=""):
    results.append((tc, desc, bool(ok), detail))


def pull(skill, cid, out_dir):
    path = os.path.join(out_dir, cid + ".xml")
    subprocess.run(["bash", os.path.join(skill, "scripts", "boomi-component-pull.sh"),
                    "--component-id", cid, "--target-path", path],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return ET.parse(path).getroot()


def local(tag):
    return tag.rsplit("}", 1)[-1]


def main(skill):
    with tempfile.TemporaryDirectory() as tmp:
        proc = pull(skill, PROCESS_ID, tmp)
        prof = pull(skill, PROFILE_ID, tmp)
        wss = pull(skill, WSS_OP_ID, tmp)
        kop = pull(skill, KAFKA_OP_ID, tmp)
        api = pull(skill, API_ID, tmp)

    comps = [proc, prof, wss, kop, api]
    shapes = list(proc.iter("shape"))
    by_name = {s.get("name"): s for s in shapes}
    types = [s.get("shapetype") for s in shapes]
    p = proc.find(".//process")

    # --- Naming and structure
    check("TC-10.1", "Process name follows Publisher convention", proc.get("name") == PROCESS_NAME, proc.get("name"))
    check("TC-10.2", "All components in agreed folder",
          all(c.get("folderFullPath") == FOLDER for c in comps),
          ", ".join(sorted({c.get("folderFullPath") for c in comps})))

    # --- Build rules
    tc_count = types.count("catcherrors")
    check("TC-10.3", "Has Try/Catch, at most three", 1 <= tc_count <= 3, f"{tc_count} Try/Catch")
    check("TC-10.4", "No Notify shapes", "notify" not in types)
    check("TC-10.5", "No scripting", "dataprocess" not in types and not list(proc.iter("dataprocessscript")))
    check("TC-10.6", "WSS start deployed in bridge mode", p.get("workload") == "bridge", p.get("workload"))
    check("TC-10.7", "Listener allows simultaneous executions", p.get("allowSimultaneous") == "true")
    start = next(s for s in shapes if s.get("shapetype") == "start")
    ca = start.find(".//connectoraction")
    check("TC-10.8", "Start is WSS Listen on the leads operation",
          ca is not None and ca.get("connectorType") == "wss" and ca.get("actionType") == "Listen"
          and ca.get("operationId") == WSS_OP_ID)

    # --- Try path
    catch = next(s for s in shapes if s.get("shapetype") == "catcherrors")
    ce = catch.find(".//catcherrors")
    check("TC-10.9", "Try/Catch catches all and retries 3 times (doc: retry 3x on connectivity errors)",
          ce.get("catchAll") == "true" and ce.get("retryCount") == "3", f"retryCount={ce.get('retryCount')}")
    produce = [s for s in shapes if (s.find(".//connectoraction") is not None
                                     and s.find(".//connectoraction").get("actionType") == "PRODUCE")]
    check("TC-10.10", "Kafka PRODUCE uses [Confluent_NL-HQ_Kafka] and the leads operation",
          len(produce) == 1 and produce[0].find(".//connectoraction").get("connectionId") == KAFKA_CONN_ID
          and produce[0].find(".//connectoraction").get("operationId") == KAFKA_OP_ID)
    props = {d.get("propertyId"): d for d in proc.iter("documentproperty")}
    topic = props.get("connector.kafka.topic_name")
    tp = topic.find(".//processparameter") if topic is not None else None
    check("TC-10.11", "Topic set from extensible DPP_KAFKA_TOPIC, default " + TOPIC,
          tp is not None and tp.get("processproperty") == "DPP_KAFKA_TOPIC"
          and tp.get("processpropertydefaultvalue") == TOPIC)
    key = props.get("connector.kafka.message_key")
    ke = key.find(".//profileelement") if key is not None else None
    check("TC-10.12", "Kafka message key is the email (tracking field)",
          ke is not None and ke.get("elementId") == "6" and ke.get("profileId") == PROFILE_ID)

    # --- Catch path: DDP_MED_NS_Msg set, then facade
    msg = props.get("dynamicdocument.DDP_MED_NS_Msg")
    mt = msg.find(".//trackparameter") if msg is not None else None
    check("TC-10.13", "DDP_MED_NS_Msg = Try/Catch message",
          mt is not None and mt.get("propertyId") == "meta.base.catcherrorsmessage")
    catch_target = next(d.get("toShape") for d in catch.iter("dragpoint") if d.get("identifier") == "error")
    reachable, todo = set(), [catch_target]
    while todo:
        n = todo.pop()
        if n in reachable or n not in by_name:
            continue
        reachable.add(n)
        todo += [d.get("toShape") for d in by_name[n].iter("dragpoint")]
    calls = [by_name[n].find(".//processcall") for n in reachable if by_name[n].get("shapetype") == "processcall"]
    check("TC-10.14", "Catch path calls [MED] (sub) CACHE Notification Facade (framework 4.0 copy)",
          any(c.get("processId") == FACADE_ID and c.get("wait") == "true" and c.get("abort") == "true" for c in calls))
    first = by_name[catch_target]
    check("TC-10.15", "DDP_MED_NS_Msg is set before the facade call",
          first.find(".//documentproperty[@propertyId='dynamicdocument.DDP_MED_NS_Msg']") is not None)
    check("TC-10.16", "Catch path ends in Exception so the caller gets an error",
          any(by_name[n].get("shapetype") == "exception" for n in reachable))

    # --- Extensions
    ov = proc.find(".//Overrides")
    conn = ov.find(f"./Connections/ConnectionOverride[@id='{KAFKA_CONN_ID}']") if ov is not None else None
    fields = list(conn.iter("field")) if conn is not None else []
    check("TC-10.17", "Kafka connection fields externalised with xpath bindings",
          len(fields) >= 9 and all(f.get("overrideable") == "true" and f.get("xpath") for f in fields),
          f"{len(fields)} fields")
    check("TC-10.18", "DPP_KAFKA_TOPIC declared as extension",
          ov is not None and ov.find("./Properties/PropertyOverride[@name='DPP_KAFKA_TOPIC']") is not None)

    # --- Tracking fields on connectors
    for tc, op, label in (("TC-12.1", wss, "WSS listen"), ("TC-12.2", kop, "Kafka produce")):
        tf = {t.get("fieldName"): t for t in op.iter("TrackedField")}
        pv = tf.get("primaryvalue")
        pe = pv.find(".//profileelement") if pv is not None else None
        sk = tf.get("primarykey")
        sp = sk.find(".//staticparameter") if sk is not None else None
        check(tc, f"{label} operation tracks primarykey=Email, primaryvalue=email",
              sp is not None and sp.get("staticproperty") == "Email"
              and pe is not None and pe.get("elementId") == "6" and pe.get("profileId") == PROFILE_ID)

    # --- Operations, profile, API
    wa = wss.find(".//WebServicesServerListenAction")
    check("TC-10.19", "WSS operation: JSON in, leads request profile",
          wa.get("inputType") == "singlejson" and wa.get("requestProfile") == PROFILE_ID)
    gc = kop.find(".//GenericOperationConfig")
    check("TC-10.20", "Kafka operation is PRODUCE to " + TOPIC,
          gc.get("customOperationType") == "PRODUCE" and gc.get("objectTypeId") == TOPIC)
    names = {e.get("name") for e in prof.iter() if local(e.tag) == "JSONObjectEntry"}
    check("TC-10.21", "Request profile has all 10 design-doc fields",
          set(PROFILE_FIELDS) <= names, ", ".join(sorted(set(PROFILE_FIELDS) - names)) or "")
    ws = api.find(".//webservice")
    route = api.find(".//route")
    check("TC-10.22", "API Service Component routes POST /gb-cg/leads to the process",
          ws.get("urlPath") == "gb-cg" and route.get("processId") == PROCESS_ID
          and route.find("overrides").get("httpMethod") == "POST")

    width = max(len(r[1]) for r in results)
    for tc, desc, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}  {tc:<9} {desc:<{width}}  {detail}")
    failed = sum(1 for r in results if not r[2])
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "/root/.claude/skills/boomi-integration"))
