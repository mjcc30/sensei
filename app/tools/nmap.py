import subprocess
import shutil
import xml.etree.ElementTree as ET
import json

class NmapTool:
    name = "nmap_scan"
    description = "Scans a target IP for open ports and services using Nmap."
    
    def run(self, target: str, quick: bool = True) -> str:
        """
        Executes an Nmap scan and returns a simplified JSON summary.
        """
        if not shutil.which("nmap"):
            return json.dumps({"error": "nmap is not installed on the host system."})
            
        # Security: Basic sanitization (very rudimentary)
        if any(c in target for c in [";", "&", "|", "`", "$"]):
            return json.dumps({"error": "Invalid characters in target"})

        args = ["nmap", target, "-oX", "-"]
        if quick:
            args.extend(["-F", "-T4"]) # Fast scan (Top 100 ports)
        else:
            args.extend(["-sV"]) # Service version detection
            
        try:
            result = subprocess.run(args, capture_output=True, text=True, timeout=300)
            if result.returncode != 0:
                return json.dumps({"error": f"Nmap failed: {result.stderr}"})
            
            return self._parse_xml_to_json(result.stdout)
        except Exception as e:
            return json.dumps({"error": f"Execution Error: {str(e)}"})

    def _parse_xml_to_json(self, xml_content: str) -> str:
        """Parses Nmap XML output to a clean JSON string for the LLM."""
        try:
            root = ET.fromstring(xml_content)
            scan_result = {"target": "", "ports": []}
            
            for host in root.findall("host"):
                # Get IP
                address = host.find("address")
                if address is not None:
                    scan_result["target"] = address.get("addr")
                
                # Get Ports
                ports = host.find("ports")
                if ports is not None:
                    for port in ports.findall("port"):
                        port_id = port.get("portid")
                        state = port.find("state").get("state")
                        service = port.find("service")
                        service_name = service.get("name") if service is not None else "unknown"
                        
                        if state == "open":
                            scan_result["ports"].append({
                                "port": port_id,
                                "service": service_name
                            })
            
            return json.dumps(scan_result, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Parsing Error: {str(e)}", "raw_output": xml_content[:500]})
