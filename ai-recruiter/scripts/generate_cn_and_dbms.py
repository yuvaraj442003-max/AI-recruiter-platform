"""
Generates unabridged master textbooks for:
- Computer Networks (cn_master.py)
- Database Management Systems (dbms_master.py)
"""
import os
import ast

TEXTBOOK_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "app", "services", "textbooks"))

# =============================================================================
# COMPUTER NETWORKS
# =============================================================================
CN_CODE = r'''"""
cn_master.py — Prescribed Master Textbook for Computer Networks (CN).
Comprehensive unabridged campus placement textbook covering OSI 7-layer model,
TCP/IP architecture, framing & CRC error detection, sliding window flow control,
IPv4/IPv6, CIDR subnetting math, routing algorithms (Dijkstra, Bellman-Ford),
TCP reliability & congestion control, HTTP/1.1 vs HTTP/2 vs HTTP/3 (QUIC), DNS,
TLS 1.3 cryptographic handshake, solved numericals, and placement interview questions.
"""

CN_MASTER_CHAPTERS = [
    {
        "chapter_num": 1,
        "title": "OSI 7-Layer Reference Model vs TCP/IP Protocol Architecture",
        "topics": [
            "Physical, Data Link, Network, Transport, Session, Presentation, Application layers",
            "Protocol Data Units (PDUs): Bits, Frames, Packets, Segments, Messages",
            "Encapsulation and decapsulation headers across network interfaces",
            "Hardware (MAC) vs Logical (IP) vs Port (Process) addressing hierarchy",
            "Network devices: Hubs (L1), Switches & Bridges (L2), Routers & Gateways (L3)"
        ],
        "key_takeaways": "Each layer provides services to the layer above and consumes services from the layer below. Routers operate at Layer 3 (Network); Switches operate at Layer 2 (Data Link)."
    },
    {
        "chapter_num": 2,
        "title": "Data Link Layer, Framing & Error Control Protocols",
        "topics": [
            "Framing techniques: Character count, Byte stuffing, and Bit stuffing (flag 01111110)",
            "Error detection algorithms: Parity check, Checksum, and Cyclic Redundancy Check (CRC-32)",
            "Flow control mechanisms: Stop-and-Wait, Go-Back-N (GBN), and Selective Repeat (SR)",
            "Medium Access Control (MAC): CSMA/CD (Ethernet collision detection) and CSMA/CA (Wi-Fi)",
            "Minimum frame size theorem in CSMA/CD: L >= 2 * Propagation Time * Bandwidth"
        ],
        "key_takeaways": "CRC uses polynomial long division over Galois Field GF(2). In Go-Back-N, receiver window is 1; in Selective Repeat, sender and receiver windows are both 2^(m-1), retransmitting only erroneous frames."
    },
    {
        "chapter_num": 3,
        "title": "Network Layer: IPv4, IPv6, Subnetting & Routing Protocols",
        "topics": [
            "IPv4 header structure (TTL, Flags, Fragmentation fields) and IPv6 improvements",
            "Classless Inter-Domain Routing (CIDR) subnet mask calculations and VLSM partitioning",
            "Address Resolution Protocol (ARP) and Network Address Translation (NAT / PAT)",
            "Distance Vector Routing (Bellman-Ford, Count-to-Infinity problem & Split Horizon)",
            "Link State Routing (Dijkstra's Shortest Path First, OSPF, Link State Advertisements)"
        ],
        "key_takeaways": "Subnet mask /26 divides a network into 4 subnets with 64 IP addresses each (62 usable host addresses). TTL prevents packets from circulating indefinitely in routing loops."
    },
    {
        "chapter_num": 4,
        "title": "Transport Layer: TCP Reliability, Flow & Congestion Control",
        "topics": [
            "TCP (connection-oriented, reliable, byte-stream) vs UDP (connectionless, datagram)",
            "TCP 3-Way Handshake (SYN -> SYN-ACK -> ACK) and 4-Way Connection Teardown (FIN -> ACK)",
            "TIME_WAIT state rationale (2 * MSL) to ensure duplicate packets dissipate",
            "Flow control via Sliding Window and Nagle's algorithm (Silly Window syndrome)",
            "Congestion Control state machine: Slow Start, Congestion Avoidance, Fast Retransmit, Fast Recovery"
        ],
        "key_takeaways": "Flow control prevents sender from overwhelming receiver (via Receiver Window rwnd); Congestion control prevents sender from overwhelming network intermediate routers (via Congestion Window cwnd)."
    },
    {
        "chapter_num": 5,
        "title": "Application Layer Protocols: HTTP, DNS, TLS & WebSockets",
        "topics": [
            "Evolution of web protocols: HTTP/1.1 (pipelining, head-of-line blocking) vs HTTP/2 (multiplexing) vs HTTP/3 (QUIC / UDP)",
            "Domain Name System (DNS) recursive vs iterative query resolution flow",
            "Transport Layer Security (TLS 1.3) cryptographic handshake and certificate verification",
            "WebSockets full-duplex persistent bidirectional communication vs HTTP polling",
            "Email protocols: SMTP (push, port 25/587) vs IMAP/POP3 (pull, port 993/995)"
        ],
        "key_takeaways": "HTTP/2 introduces binary framing and stream multiplexing over a single TCP connection, but suffers from TCP-level head-of-line blocking. HTTP/3 resolves this by running over QUIC (UDP)."
    },
    {
        "chapter_num": 6,
        "title": "Solved Networking Placement Numericals & Interview Drills",
        "topics": [
            "Subnetting & VLSM IP allocation numericals",
            "CRC error detection generator polynomial step-by-step division",
            "Sliding window protocol efficiency & throughput calculations",
            "CSMA/CD minimum frame length determination for high-speed Ethernet",
            "TCP sequence number arithmetic and congestion window tracing"
        ],
        "key_takeaways": "Mastering subnet mask conversion, CRC bit-shifting, and TCP sequence/ACK number tracing guarantees high scores in technical tests for Cisco, Amazon, Google, and TCS Digital."
    }
]

CN_TEXTBOOK_MARKDOWN = r"""# Computer Networks & Internet Protocols: Complete Master Edition (Prescribed Textbook)

**Edition:** 2026 Campus Placement Edition  
**Subject:** Computer Networks (CN)  
**Courseware Board:** Prescribed Placement Architectural Board  
**Status:** In-App Complete Master Textbook (Full Curriculum Available In-Platform)

> **🔒 EXAM GROUNDING POLICY:** All campus placement assessments, network engineering technical interviews, and online test questions are strictly grounded in the protocols, layer models, subnetting formulas, and RFC standards detailed in this textbook.

---

## 📑 Complete Table of Contents

- [Chapter 1: OSI 7-Layer Reference Model vs TCP/IP Protocol Architecture](#chapter-1-osi-7-layer-reference-model-vs-tcpip-protocol-architecture)
  - [1.1 The Theoretical OSI 7-Layer Architecture](#11-the-theoretical-osi-7-layer-architecture)
  - [1.2 Protocol Data Units (PDUs) & Encapsulation Stack](#12-protocol-data-units-pdus--encapsulation-stack)
  - [1.3 Hardware Devices by Layer: Hubs, Switches, Routers & Gateways](#13-hardware-devices-by-layer-hubs-switches-routers--gateways)
  - [1.4 The 4-Layer TCP/IP Real-World Model](#14-the-4-layer-tcpip-real-world-model)
- [Chapter 2: Data Link Layer, Framing & Error Control Protocols](#chapter-2-data-link-layer-framing--error-control-protocols)
  - [2.1 Framing Mechanics: Byte Stuffing & Bit Stuffing](#21-framing-mechanics-byte-stuffing--bit-stuffing)
  - [2.2 Error Detection: Parity, Checksum & CRC Polynomial Math](#22-error-detection-parity-checksum--crc-polynomial-math)
  - [2.3 Flow Control: Stop-and-Wait, Go-Back-N & Selective Repeat](#23-flow-control-stop-and-wait-go-back-n--selective-repeat)
  - [2.4 Medium Access Control: CSMA/CD & CSMA/CA](#24-medium-access-control-csmacd--csmaca)
- [Chapter 3: Network Layer: IPv4, IPv6, Subnetting & Routing Protocols](#chapter-3-network-layer-ipv4-ipv6-subnetting--routing-protocols)
  - [3.1 IPv4 Header Architecture & Packet Fragmentation](#31-ipv4-header-architecture--packet-fragmentation)
  - [3.2 CIDR Subnetting Math & VLSM Design](#32-cidr-subnetting-math--vlsm-design)
  - [3.3 Address Resolution Protocol (ARP) & NAT/PAT](#33-address-resolution-protocol-arp--natpat)
  - [3.4 Routing Protocols: Distance Vector vs Link State Routing](#34-routing-protocols-distance-vector-vs-link-state-routing)
- [Chapter 4: Transport Layer: TCP Reliability, Flow & Congestion Control](#chapter-4-transport-layer-tcp-reliability-flow--congestion-control)
  - [4.1 TCP vs UDP Architectural Comparison](#41-tcp-vs-udp-architectural-comparison)
  - [4.2 TCP 3-Way Handshake & 4-Way Teardown (TIME_WAIT Deep Dive)](#42-tcp-3-way-handshake--4-way-teardown-timewait-deep-dive)
  - [4.3 Sliding Window Flow Control & Silly Window Prevention](#43-sliding-window-flow-control--silly-window-prevention)
  - [4.4 TCP Congestion Control State Machine](#44-tcp-congestion-control-state-machine)
- [Chapter 5: Application Layer Protocols: HTTP, DNS, TLS & WebSockets](#chapter-5-application-layer-protocols-http-dns-tls--websockets)
  - [5.1 The Evolution of Web Protocols: HTTP/1.1 vs HTTP/2 vs HTTP/3](#51-the-evolution-of-web-protocols-http11-vs-http2-vs-http3)
  - [5.2 Domain Name System (DNS) Architecture](#52-domain-name-system-dns-architecture)
  - [5.3 Transport Layer Security (TLS 1.3) Cryptographic Handshake](#53-transport-layer-security-tls-13-cryptographic-handshake)
  - [5.4 WebSockets Full-Duplex Real-Time Communication](#54-websockets-full-duplex-real-time-communication)
- [Chapter 6: Solved Networking Placement Numericals & Interview Drills](#chapter-6-solved-networking-placement-numericals--interview-drills)
  - [Solved Problem 1: CIDR VLSM Subnet Allocation](#solved-problem-1-cidr-vlsm-subnet-allocation)
  - [Solved Problem 2: CRC-32 Frame Generation & Check](#solved-problem-2-crc-32-frame-generation--check)
  - [Solved Problem 3: CSMA/CD Minimum Packet Size Determination](#solved-problem-3-csmacd-minimum-packet-size-determination)
  - [Self-Assessment Practice Exercises & Verified Solutions](#self-assessment-practice-exercises--verified-solutions)

---

## Chapter 1: OSI 7-Layer Reference Model vs TCP/IP Protocol Architecture

### 1.1 The Theoretical OSI 7-Layer Architecture
The Open Systems Interconnection (OSI) model was developed by the International Organization for Standardization (ISO) in 1984 as an architectural blueprint for open communication between disparate computer systems. The 7 layers, numbered bottom-up from Layer 1 to Layer 7:

```
[ Layer 7: Application  ] -> End-user applications, APIs (HTTP, DNS, SSH, FTP, SMTP)
[ Layer 6: Presentation ] -> Syntax, data formatting, encryption (TLS), compression (JPEG)
[ Layer 5: Session      ] -> Dialog management, token management, session sync (Sockets, RPC)
[ Layer 4: Transport    ] -> End-to-end reliability, segmentation, port addressing (TCP, UDP)
[ Layer 3: Network      ] -> Logical routing, logical addressing, path selection (IPv4, IPv6, ICMP)
[ Layer 2: Data Link    ] -> Physical addressing (MAC), framing, hop-to-hop flow/error control
[ Layer 1: Physical     ] -> Bitstream transmission over physical media (Cables, Fiber, RF)
```

### 1.2 Protocol Data Units (PDUs) & Encapsulation Stack
As application data travels down the protocol stack on the sending host, each layer prepends a header containing metadata (and occasionally appends a trailer), a process known as **Encapsulation**:

1. **Application Data:** Raw message generated by the user application (e.g., `GET /index.html HTTP/1.1`).
2. **Transport Layer PDU:** Adds a TCP or UDP header containing Source Port (16-bit) and Destination Port (16-bit). The PDU is termed a **Segment** (TCP) or **Datagram** (UDP).
3. **Network Layer PDU:** Adds an IP header containing Source IP (32-bit for IPv4) and Destination IP (32-bit). The PDU is termed a **Packet**.
4. **Data Link Layer PDU:** Adds a MAC header containing Source MAC (48-bit) and Destination MAC (48-bit), plus an FCS (Frame Check Sequence) trailer. The PDU is termed a **Frame**.
5. **Physical Layer PDU:** The frame is encoded into electromagnetic or optical signals as raw **Bits**.

On the receiving host, the process is reversed (**Decapsulation**): each layer strips its corresponding header, verifies checksums, and dispatches the payload to the appropriate entity in the layer above.

### 1.3 Hardware Devices by Layer: Hubs, Switches, Routers & Gateways
| Device | Operating OSI Layer | Addressing Scheme | Collision Domain | Broadcast Domain | Functionality |
|:---|:---|:---|:---|:---|:---|
| **Hub / Repeater** | Layer 1 (Physical) | None (Blind Electrical) | 1 Shared Collision Domain | 1 Shared Broadcast Domain | Amplifies and broadcasts electrical signals to all connected physical ports. |
| **Bridge / Switch** | Layer 2 (Data Link) | 48-bit MAC Addresses | Separate Collision Domain per port | 1 Shared Broadcast Domain | Maintains a CAM (Content Addressable Memory) MAC address table to forward frames selectively. |
| **Router** | Layer 3 (Network) | 32-bit IPv4 / 128-bit IPv6 | Separate Collision Domain per port | Separate Broadcast Domain per interface | Evaluates routing tables to forward packets across subnet boundaries. |
| **Gateway / Proxy** | Layer 4-7 (Application) | IP + Port + Protocol payload | Isolated | Isolated | Performs application-layer protocol translation, load balancing, or deep packet inspection. |

---

## Chapter 2: Data Link Layer, Framing & Error Control Protocols

### 2.1 Framing Mechanics: Byte Stuffing & Bit Stuffing
To allow the receiver to recognize frame boundaries, the sender encapsulates frames between delimiter patterns:

- **Byte Stuffing (Character-Oriented Framing):**
  Uses special control bytes `FLAG` (e.g., `0x7E`) and `ESC` (Escape, e.g., `0x7D`). Whenever `FLAG` or `ESC` occurs inside the data payload, an `ESC` byte is prepended. The receiver removes the escape byte upon reception.

- **Bit Stuffing (Bit-Oriented Framing, HDLC / PPP):**
  The flag sequence is strictly `01111110` (six consecutive 1s).
  - **Rule:** Whenever the sender detects five consecutive 1s (`11111`) in the data stream, it unconditionally inserts (stuffs) a `0` bit immediately after the fifth 1.
  - **Receiver Logic:** When five consecutive 1s are encountered:
    - If the next bit is `0`, it is discarded (unstuffed) as an inserted padding bit.
    - If the next bit is `1` followed by `0`, a `FLAG` delimiter is detected (`01111110`).
    - If the next bit is `1` followed by `1`, an error (abort condition) has occurred.

### 2.2 Error Detection: Parity, Checksum & CRC Polynomial Math
Error detection protects frames from channel noise bit-flips without requiring retransmission of all bits.

#### Cyclic Redundancy Check (CRC) Polynomial Division
CRC treats binary data strings as polynomials over Galois Field $GF(2)$ where addition and subtraction are equivalent to the bitwise XOR operation (no carry or borrow).

**Algorithm for Sender Frame Generation:**
1. Let the original data string have $m$ bits.
2. Let the generator polynomial $G(x)$ have degree $r$ (length $r + 1$ bits).
3. Append $r$ zero bits to the end of the data string.
4. Perform binary polynomial division of the appended data by $G(x)$ using XOR subtraction.
5. The $r$-bit remainder is the CRC Checksum (FCS). Replace the appended $r$ zeroes with this remainder to construct the transmitted frame.

**Verification at Receiver:**
The receiver divides the entire received frame by $G(x)$. If the remainder is all zeroes, the frame is error-free; otherwise, a transmission bit error occurred and the frame is discarded.

### 2.3 Flow Control: Stop-and-Wait, Go-Back-N & Selective Repeat
Flow control matches the transmission rate of the sender to the processing speed of the receiver.

Let $T_t = \frac{L}{B}$ be Transmission Time (Packet length $L$ over Bandwidth $B$).  
Let $T_p = \frac{d}{v}$ be Propagation Delay (Distance $d$ over Propagation velocity $v$).  
Let $a = \frac{T_p}{T_t}$ be the propagation-to-transmission ratio.

$$\text{Efficiency } \eta = \frac{N}{1 + 2a}, \quad \text{where } N \text{ is the sender window size}$$

| Protocol | Sender Window Size ($W_s$) | Receiver Window Size ($W_r$) | Sequence Numbers Required ($m$ bits) | Out-of-Order Frames Accepted? | Retransmission Mechanism |
|:---|:---|:---|:---|:---|:---|
| **Stop-and-Wait** | $1$ | $1$ | At least $2$ ($0$ and $1$) | No | Retransmits last unacknowledged frame upon timer expiration. Efficiency: $\frac{1}{1 + 2a}$. |
| **Go-Back-N (GBN)** | $2^m - 1$ | $1$ | $2^m$ | No (Discarded) | Cumulative ACKs. On timeout of frame $k$, retransmits frame $k$ and all subsequent frames in the window. |
| **Selective Repeat (SR)** | $2^{m-1}$ | $2^{m-1}$ | $2^m$ | Yes (Buffered in receiver window) | Individual (Selective) ACKs / NAKs. Retransmits only the single lost or corrupted frame. |

### 2.4 Medium Access Control: CSMA/CD & CSMA/CA
#### Carrier Sense Multiple Access with Collision Detection (CSMA/CD)
Used in legacy half-duplex Ethernet (IEEE 802.3):
1. **Carrier Sense:** Listen before transmit. If channel is busy, wait; if idle, transmit.
2. **Collision Detection:** Listen while transmitting. If signal energy exceeds normal threshold, a collision has occurred.
3. **Jam Signal & Backoff:** If collision detected, transmit a 32-bit Jam signal and execute the **Truncated Binary Exponential Backoff Algorithm**:
   $$K \in [0, 2^{\min(n, 10)} - 1], \quad \text{Wait Time } = K \times 2T_p \text{ (slot time)}$$
   After 16 consecutive collisions ($n = 16$), the transmission is aborted.

**Fundamental CSMA/CD Condition:** The sender must still be transmitting when the collision signal from the farthest possible station arrives back at the sender:
$$T_t \ge 2 \times T_p \implies \frac{L_{\min}}{B} \ge 2 \times \frac{d}{v} \implies L_{\min} \ge 2 \times T_p \times B$$

---

## Chapter 3: Network Layer: IPv4, IPv6, Subnetting & Routing Protocols

### 3.1 IPv4 Header Architecture & Packet Fragmentation
An IPv4 header has a minimum length of 20 bytes (when IHL = 5) and a maximum length of 60 bytes (IHL = 15).

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|  IHL  |Type of Service|          Total Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Identification        |Flags|     Fragment Offset     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Time to Live |    Protocol   |        Header Checksum        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Source IP Address                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Destination IP Address                     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

- **IHL (Internet Header Length):** 4 bits, measured in 4-byte (32-bit) words. Minimum is 5 ($5 \times 4 = 20\text{ bytes}$).
- **Total Length:** 16 bits, specifies total length of packet (header + payload) in bytes. Maximum packet size $= 2^{16} - 1 = 65,535\text{ bytes}$.
- **Flags (3 bits):**
  - Bit 0: Reserved (must be 0).
  - Bit 1: **DF (Don't Fragment):** If set to 1 and packet > MTU, router drops packet and returns ICMP "Destination Unreachable (Fragmentation Needed)".
  - Bit 2: **MF (More Fragments):** 1 indicates more fragments follow; 0 indicates this is the final fragment.
- **Fragment Offset (13 bits):** Position of fragment payload relative to the original unfragmented packet, measured in **8-byte units** (must be divisible by 8).
- **Time to Live (TTL):** 8 bits, decremented by 1 at every router hop. Prevents infinite looping in routing loops. When TTL reaches 0, router drops packet and sends ICMP "Time Exceeded" (Type 11), the mechanism powering `traceroute`.

### 3.2 CIDR Subnetting Math & VLSM Design
In Classless Inter-Domain Routing (RFC 1519), addresses are written as `a.b.c.d/n`, where `/n` denotes the network prefix length:
- **Network Bits:** $n$
- **Host Bits:** $h = 32 - n$
- **Total Addresses in Block:** $2^h = 2^{32 - n}$
- **Usable Host Addresses:** $2^h - 2$ (Subtracting Network Address where all host bits are `0`, and Directed Broadcast Address where all host bits are `1`).

```
CIDR Prefix Table Reference:
/24 -> 255.255.255.0   -> 2^8  = 256 Total IPs -> 254 Usable Hosts
/25 -> 255.255.255.128 -> 2^7  = 128 Total IPs -> 126 Usable Hosts
/26 -> 255.255.255.192 -> 2^6  = 64  Total IPs -> 62  Usable Hosts
/27 -> 255.255.255.224 -> 2^5  = 32  Total IPs -> 30  Usable Hosts
/28 -> 255.255.255.240 -> 2^4  = 16  Total IPs -> 14  Usable Hosts
/29 -> 255.255.255.248 -> 2^3  = 8   Total IPs -> 6   Usable Hosts
/30 -> 255.255.255.252 -> 2^2  = 4   Total IPs -> 2   Usable Hosts (Point-to-Point links)
```

### 3.3 Address Resolution Protocol (ARP) & NAT/PAT
- **ARP (RFC 826):** Resolves a known Layer 3 logical IP address to a physical Layer 2 MAC address.
  - An ARP Request is a **Broadcast frame** (`FF:FF:FF:FF:FF:FF`) asking: "Who has IP 192.168.1.5? Tell 192.168.1.1".
  - The destination node replies with an **ARP Reply** sent as a **Unicast frame** containing its hardware MAC address.
  - Results are cached in the host's ARP cache table.
- **NAT / PAT (Port Address Translation):** Maps hundreds of private internal IP addresses (RFC 1918: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) to a single public IP address using ephemeral source ports (1024-65535).

### 3.4 Routing Protocols: Distance Vector vs Link State Routing
| Feature | Distance Vector (RIP) | Link State (OSPF) |
|:---|:---|:---|
| **Underlying Algorithm** | Bellman-Ford equation: $D_x(y) = \min_v \{c(x,v) + D_v(y)\}$ | Dijkstra's Shortest Path First (SPF) algorithm |
| **Information Shared** | Vector of distances to all destinations, shared only with immediate direct neighbors. | Entire network topology (Link State Advertisements), flooded to all routers in the AS. |
| **Convergence Speed** | Slow; susceptible to the **Count-to-Infinity problem** when a link fails. | Rapid convergence; updates sent only upon link-state changes. |
| **Loop Prevention** | Split Horizon and Poison Reverse techniques. | Complete graph topology prevents loops mathematically. |

---

## Chapter 4: Transport Layer: TCP Reliability, Flow & Congestion Control

### 4.1 TCP vs UDP Architectural Comparison
| Parameter | Transmission Control Protocol (TCP) | User Datagram Protocol (UDP) |
|:---|:---|:---|
| **Connection Orientation** | Connection-oriented (3-way handshake) | Connectionless (fire and forget) |
| **Reliability** | Guaranteed delivery via ACKs and retransmissions | Best-effort; no retransmission or delivery guarantee |
| **Ordering** | In-order delivery guaranteed via sequence numbers | Unordered arrival; datagrams can arrive out of sequence |
| **Header Overhead** | 20 to 60 bytes | Strictly 8 bytes fixed |
| **Flow & Congestion Control** | Full sliding window and congestion state machines | None; sends packets at rate provided by application |
| **Typical Use Cases** | Web (HTTP/1.1, HTTP/2), Email (SMTP), SSH, File transfers | Streaming video, VoIP, DNS queries, Online gaming, HTTP/3 |

### 4.2 TCP 3-Way Handshake & 4-Way Teardown (TIME_WAIT Deep Dive)

```
        Client                                   Server
          |                                        |
          | ---------- SYN (seq = x) ------------> | (Server enters SYN-RECEIVED)
          | <--- SYN-ACK (seq = y, ack = x + 1) -- | (Client enters ESTABLISHED)
          | ---------- ACK (ack = y + 1) --------> | (Server enters ESTABLISHED)
          |                                        |
      [DATA TRANSFER OCCURS OVER DUPLEX CONNECTION]
          |                                        |
          | ---------- FIN (seq = u) ------------> | (Server enters CLOSE-WAIT)
          | <--------- ACK (ack = u + 1) --------- | (Client enters FIN-WAIT-2)
          | <--------- FIN (seq = v) ------------- | (Server enters LAST-ACK)
          | ---------- ACK (ack = v + 1) --------> | (Server enters CLOSED)
          |                                        |
          | [Client enters TIME_WAIT: 2 * MSL]     |
          | [Expires after 120s -> Enters CLOSED]  |
```

**Why TIME_WAIT is Mandatory (2 * Maximum Segment Lifetime):**
1. **Ensure Final ACK Delivery:** If the client's final ACK is lost in transit, the server retransmits its FIN. The client must still be alive in TIME_WAIT to re-acknowledge the FIN, avoiding a reset `RST`.
2. **Dissipate Old Duplicate Segments:** Prevents stray duplicate packets from the terminated connection from being mistakenly accepted by a new connection reusing the same IP/Port socket 4-tuple.

### 4.3 Sliding Window Flow Control & Silly Window Prevention
- **Flow Control Mechanism:** The receiver advertises its available buffer space via the 16-bit `rwnd` (Receiver Window) field in every TCP header. The sender guarantees that:
  $$\text{Bytes In Flight} \le \min(\text{cwnd}, \text{rwnd})$$
- **Silly Window Syndrome:** If a slow application reads data 1 byte at a time, the receiver window opens by 1 byte, causing the sender to transmit tiny 1-byte packets wrapped in 40-byte TCP/IP headers (overhead > 97%).
  - **Receiver Fix (Clark's Solution):** Prevent advertising small windows until the buffer can receive either a full MSS (Maximum Segment Size) or half the buffer space.
  - **Sender Fix (Nagle's Algorithm):** If unacknowledged data is in flight, buffer outgoing user data until a full MSS accumulates or an ACK arrives.

### 4.4 TCP Congestion Control State Machine
TCP maintains `cwnd` (Congestion Window) and `ssthresh` (Slow Start Threshold):

```
State Machine Transition Flow:
1. Slow Start (cwnd < ssthresh):
   - cwnd initialized to 1 MSS (or initial window 10 MSS in modern Linux).
   - Upon each ACK: cwnd = cwnd + 1 MSS (Doubles cwnd every RTT -> Exponential growth: 1 -> 2 -> 4 -> 8 -> 16).

2. Congestion Avoidance (cwnd >= ssthresh):
   - Upon each RTT: cwnd = cwnd + (1 / cwnd) * 1 MSS (Linear growth: +1 MSS per RTT -> Additive Increase).

3. Packet Loss Event - Triple Duplicate ACKs:
   - Fast Retransmit: Immediately resends the missing segment without waiting for the retransmission timer.
   - Fast Recovery:
     ssthresh = cwnd / 2
     cwnd = ssthresh + 3 MSS (Multiplicative Decrease)
     Continues linear Congestion Avoidance upon new ACK.

4. Packet Loss Event - Retransmission Timeout (RTO):
   - Indicates severe network collapse.
   - ssthresh = cwnd / 2
   - cwnd is reset to 1 MSS
   - Restarts Slow Start from the beginning.
```

---

## Chapter 5: Application Layer Protocols: HTTP, DNS, TLS & WebSockets

### 5.1 The Evolution of Web Protocols: HTTP/1.1 vs HTTP/2 vs HTTP/3
| Architectural Feature | HTTP/1.1 (RFC 2616) | HTTP/2 (RFC 7540) | HTTP/3 (RFC 9114) |
|:---|:---|:---|:---|
| **Transport Layer** | TCP | TCP | **QUIC (UDP)** |
| **Format** | Plaintext ASCII | Binary Framing (Frames & Streams) | Binary Framing |
| **Multiplexing** | No (Head-of-Line blocking on socket; requires multiple parallel TCP connections) | Yes (Multiple streams multiplexed over 1 single TCP connection) | Yes (Independent streams over QUIC; zero cross-stream blocking) |
| **TCP Head-of-Line Blocking** | Present | Present (If 1 TCP packet drops, all multiplexed HTTP streams stall) | **Eliminated** (Packet drop on stream A does not stall stream B) |
| **Connection Setup** | 1 RTT (TCP) + 2 RTT (TLS) = 3 RTT | 1 RTT (TCP) + 1-2 RTT (TLS) | **0-RTT or 1-RTT** (QUIC merges transport and TLS 1.3 handshake) |
| **Connection Migration** | Bound to IP/Port 4-tuple (Disconnects when Wi-Fi switches to LTE) | Bound to IP/Port 4-tuple | Supported via 64-bit Connection ID (survives network IP change) |

### 5.2 Domain Name System (DNS) Architecture
DNS resolves human-readable domain names (`recruiter.ai.edu`) into IP addresses (`142.250.190.46`). It uses UDP port 53 (and TCP port 53 for zone transfers > 512 bytes).

**Recursive Query vs Iterative Query Pathway:**
```
[Client Browser]
      |  (1) Recursive Query: "What is IP of recruiter.ai.edu?"
      v
[Local DNS Resolver / ISP (e.g., 8.8.8.8)]
      |  (2) Iterative Query: "recruiter.ai.edu"
      v
[Root Nameserver (13 logical root server clusters: a.root-servers.net)]
      |  (3) Referral: "Ask the .edu TLD server at IP x.x.x.x"
      v
[TLD Nameserver (.edu)]
      |  (4) Referral: "Ask the ai.edu Authoritative server at IP y.y.y.y"
      v
[Authoritative Nameserver (ai.edu)]
      |  (5) Answer: "recruiter.ai.edu has A record 142.250.190.46 (TTL=300)"
      v
[Local DNS Resolver Caches Result & Returns to Browser]
```

### 5.3 Transport Layer Security (TLS 1.3) Cryptographic Handshake
TLS 1.3 (RFC 8446) reduced the handshake latency from 2 RTTs (in TLS 1.2) to **1 RTT**:

1. **ClientHello:** Sends supported cipher suites, TLS version (1.3), random nonce, and the **Client Diffie-Hellman Key Share** ($g^a \bmod p$) using Elliptic Curve Cryptography (ECDHE).
2. **ServerHello:** Selects the cipher suite, sends Server random nonce, and the **Server Key Share** ($g^b \bmod p$).
   - Both client and server immediately derive the shared symmetric encryption key ($g^{ab} \bmod p$).
   - The server encrypts all subsequent handshake messages with this key.
3. **Encrypted Server Payload:** Server sends its X.509 Digital Certificate, Digital Signature over the handshake transcript, and `Finished` MAC.
4. **Client Verification:** Client verifies the server certificate against local Root Certificate Authorities (CA), validates the signature, and sends its `Finished` MAC.
5. Secure encrypted application data exchange begins.

### 5.4 WebSockets Full-Duplex Real-Time Communication
HTTP is unidirectional and request-driven. WebSockets (RFC 6455) provides persistent, bi-directional, full-duplex communication over a single TCP connection:
- Initiated via an standard HTTP/1.1 request containing headers:
  ```http
  GET /chat HTTP/1.1
  Host: server.example.com
  Upgrade: websocket
  Connection: Upgrade
  Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
  Sec-WebSocket-Version: 13
  ```
- If the server accepts, it responds with status `101 Switching Protocols`:
  ```http
  HTTP/1.1 101 Switching Protocols
  Upgrade: websocket
  Connection: Upgrade
  Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
  ```
- From this moment on, HTTP semantics are dropped and both parties exchange lightweight binary/text frames with only 2 to 10 bytes of frame framing overhead.

---

## Chapter 6: Solved Networking Placement Numericals & Interview Drills

### Solved Problem 1: CIDR VLSM Subnet Allocation
- **Problem:** An organization has been assigned the network block `172.16.0.0/22`. Design a Variable Length Subnet Mask (VLSM) scheme to allocate subnets for 3 separate departments:
  - Department A: 450 hosts
  - Department B: 200 hosts
  - Department C: 100 hosts
  Determine the subnet mask, network address, usable host IP range, and broadcast address for each department.
- **Solution:**
  1. **Department A (450 hosts):**
     - Host bits needed: $2^h - 2 \ge 450 \implies 2^9 - 2 = 510 \ge 450 \implies h = 9$.
     - Subnet prefix: $32 - 9 = \mathbf{/23}$. Subnet mask: `255.255.254.0`.
     - Network ID: `172.16.0.0/23`.
     - Usable Host Range: `172.16.0.1` to `172.16.1.254`.
     - Directed Broadcast Address: `172.16.1.255`.
     - Total addresses consumed: $2^9 = 512$ (spans `172.16.0.0` - `172.16.1.255`).
  2. **Department B (200 hosts):**
     - Next available network address: `172.16.2.0`.
     - Host bits needed: $2^h - 2 \ge 200 \implies 2^8 - 2 = 254 \ge 200 \implies h = 8$.
     - Subnet prefix: $32 - 8 = \mathbf{/24}$. Subnet mask: `255.255.255.0`.
     - Network ID: `172.16.2.0/24`.
     - Usable Host Range: `172.16.2.1` to `172.16.2.254`.
     - Directed Broadcast Address: `172.16.2.255`.
     - Total addresses consumed: $2^8 = 256$ (spans `172.16.2.0` - `172.16.2.255`).
  3. **Department C (100 hosts):**
     - Next available network address: `172.16.3.0`.
     - Host bits needed: $2^h - 2 \ge 100 \implies 2^7 - 2 = 126 \ge 100 \implies h = 7$.
     - Subnet prefix: $32 - 7 = \mathbf{/25}$. Subnet mask: `255.255.255.128`.
     - Network ID: `172.16.3.0/25`.
     - Usable Host Range: `172.16.3.1` to `172.16.3.126`.
     - Directed Broadcast Address: `172.16.3.127`.

### Solved Problem 2: CRC-32 Frame Generation & Check
- **Problem:** Data bit sequence $M = 1101011011$. Generator polynomial $G(x) = x^4 + x + 1$ (bit string `10011`). Compute the transmitted CRC codeword.
- **Solution:**
  1. Degree of $G(x)$ is $r = 4$. Append 4 zeros to data $M$: `11010110110000`.
  2. Perform polynomial division using XOR:
     ```
     11010110110000 / 10011
     11010110110000
     10011
     -----
     010011
      10011
      -----
      0000010110
            10011
            -----
            0010100
              10011
              -----
              001110
                10011
                -----
                01101 (Remainder is 1110 -> 4 bits)
     ```
  3. The 4-bit remainder (FCS) is `1110`.
  4. Transmitted frame codeword: `11010110111110`.

### Solved Problem 3: CSMA/CD Minimum Packet Size Determination
- **Problem:** A 1 Gbps ($10^9\text{ bps}$) half-duplex CSMA/CD Ethernet network has a cable length of 1 km with signal propagation speed $v = 2 \times 10^8\text{ m/s}$. Determine the minimum Ethernet frame size in bytes.
- **Solution:**
  1. Propagation time: $T_p = \frac{\text{Distance}}{v} = \frac{1000\text{ m}}{2 \times 10^8\text{ m/s}} = 5 \times 10^{-6}\text{ s} = 5\ \mu\text{s}$.
  2. Round-Trip Time: $2 \times T_p = 2 \times 5\ \mu\text{s} = 10\ \mu\text{s} = 10^{-5}\text{ s}$.
  3. For CSMA/CD collision detection:
     $$T_t \ge 2 T_p \implies \frac{L_{\min}}{\text{Bandwidth}} \ge 2 T_p$$
     $$L_{\min} = 2 \times T_p \times B = 10^{-5}\text{ s} \times 10^9\text{ bps} = 10^4\text{ bits}$$
  4. Frame size in bytes: $L_{\min} = \frac{10,000}{8} = \mathbf{1250\text{ bytes}}$.

---

### Self-Assessment Practice Exercises & Verified Solutions:

1. **Exercise 1 (TCP Sequence Arithmetic):** Host A sends 3 consecutive TCP segments of size 1460 bytes each to Host B. If the initial sequence number of the first segment is 5000, what is the sequence number and acknowledgment number in Host B's response acknowledging all three segments?
   - *Solution:* First segment spans bytes [5000 to 6459]. Second segment spans bytes [6460 to 7919]. Third segment spans bytes [7920 to 9379]. Host B acknowledges the next expected byte: $\text{ACK} = 9380$.

2. **Exercise 2 (Subnet Capacity):** What is the maximum number of usable host IP addresses in a `/21` IPv4 network?
   - *Solution:* Host bits $h = 32 - 21 = 11$. Total hosts $= 2^{11} - 2 = 2048 - 2 = \mathbf{2046\text{ usable hosts}}$.

3. **Exercise 3 (HTTP/2 vs HTTP/3):** What fundamental transport-layer limitation causes HTTP/2 to experience Head-of-Line blocking, and how does HTTP/3 overcome it?
   - *Solution:* HTTP/2 multiplexes all logical streams over a single TCP byte-stream. If one TCP packet is dropped, TCP halts delivery of all subsequent data across all streams until the missing segment is retransmitted. HTTP/3 runs on top of QUIC (UDP), where each stream maintains its own independent sequence tracking; a dropped packet in stream A has zero impact on streams B and C.

4. **Exercise 4 (Selective Repeat Window Size):** If 4 bits are allocated for sequence numbers in the frame header, what is the maximum permissible sender window size in Selective Repeat protocol to prevent duplicate frame ambiguity?
   - *Solution:* Condition for Selective Repeat: $W_s + W_r \le 2^m$. Since $W_s = W_r$, $2 W_s \le 2^m \implies W_s \le 2^{m-1} = 2^{4-1} = 2^3 = \mathbf{8}$.

5. **Exercise 5 (NAT Port Range):** Why does Port Address Translation (PAT) support up to approximately 64,000 concurrent outbound connections per public IP address?
   - *Solution:* TCP source port is a 16-bit field ($2^{16} = 65,536$ possible ports). Excluding the well-known reserved system ports (0 to 1023), approximately 64,512 ephemeral ports are available for NAT translation mappings.
"""

CN_EXPANDED_QUESTIONS = [
    {
        "chapter_num": 3,
        "chapter_title": "Network Layer: IPv4, IPv6, Subnetting & Routing Protocols",
        "subtopic": "Subnet Host Capacity",
        "question": "How many usable host IP addresses are available in a subnetwork with CIDR prefix /27?",
        "options": ["30", "32", "62", "28"],
        "correct_option_index": 0,
        "explanation": "📖 [CN Prescribed Textbook — Chapter 3: Network Layer & Subnetting]\nAn IPv4 address has 32 bits. For /27, remaining host bits = 32 - 27 = 5 bits. Total IP addresses = 2^5 = 32. Subtracting 2 (Network ID and Directed Broadcast Address) leaves exactly 30 usable host addresses.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 4,
        "chapter_title": "Transport Layer: TCP Reliability, Flow & Congestion Control",
        "subtopic": "TCP Congestion Window Growth",
        "question": "In TCP Congestion Control, how does the Congestion Window (cwnd) grow during the Slow Start phase upon receiving successful acknowledgments?",
        "options": [
            "Exponentially (doubles every Round-Trip Time)",
            "Linearly (increases by 1 MSS every RTT)",
            "Logarithmically (increases by log(cwnd))",
            "Remains constant until reaching maximum bandwidth"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [CN Prescribed Textbook — Chapter 4: Transport Layer]\nDuring Slow Start, cwnd increases by 1 MSS for every received ACK, which results in doubling the window size every RTT (exponential growth) until it hits the slow start threshold (ssthresh).",
        "difficulty": "medium",
    },
    {
        "chapter_num": 2,
        "chapter_title": "Data Link Layer, Framing & Error Control Protocols",
        "subtopic": "CSMA/CD Minimum Frame Size",
        "question": "In a CSMA/CD Ethernet network, why must the minimum transmission time of a frame be at least twice the propagation delay (Tt >= 2*Tp)?",
        "options": [
            "To ensure the sender is still transmitting when a collision signal from the farthest node returns, allowing detection",
            "To prevent the receiver buffer from overflowing",
            "To allow the router to calculate the CRC polynomial",
            "To encrypt the packet with TLS 1.3"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [CN Prescribed Textbook — Chapter 2: Data Link Layer & CSMA/CD]\nIn CSMA/CD, the transmitting station can only detect collisions while it is actively sending bits. If the frame is shorter than 2*Tp, the sender finishes sending before the collision wave arrives back, failing to detect the corrupted packet.",
        "difficulty": "hard",
    }
]
'''

# =============================================================================
# DATABASE MANAGEMENT SYSTEMS (DBMS)
# =============================================================================
DBMS_CODE = r'''"""
dbms_master.py — Prescribed Master Textbook for Database Management Systems (DBMS).
Comprehensive unabridged campus placement textbook covering 3-schema architecture,
ER modeling, relational algebra & calculus, functional dependencies, Armstrong's axioms,
1NF, 2NF, 3NF, BCNF, ACID transactions, conflict serializability, strict 2PL,
Write-Ahead Logging (WAL), ARIES recovery, B+ trees, and placement interview questions.
"""

DBMS_MASTER_CHAPTERS = [
    {
        "chapter_num": 1,
        "title": "DBMS Architecture, Relational Model & ER Modeling",
        "topics": [
            "3-Schema Architecture: Physical, Conceptual, External views & Data Independence",
            "Entity-Relationship (ER) Modeling: Strong vs Weak entities, Cardinality ratios",
            "Specialization, Generalization, Aggregation & Enhanced ER (EER) concepts",
            "Algorithm for mapping ER diagrams to Relational schemas (foreign keys, associative tables)",
            "Relational Model constraints: Domain, Key, Entity Integrity, Referential Integrity (ON DELETE CASCADE)"
        ],
        "key_takeaways": "Logical Data Independence protects conceptual schema from physical storage modifications. Weak entities have no primary key of their own and depend on an identifying owner entity via a discriminator."
    },
    {
        "chapter_num": 2,
        "title": "Relational Algebra, Tuple Calculus & Query Processing",
        "topics": [
            "Fundamental operators: Selection (sigma), Projection (pi), Union, Set Difference, Cartesian Product (X)",
            "Derived operators: Natural Join (bowtie), Theta Join, Equi-Join, Semijoin, Division (/)",
            "Outer Joins: Left Outer Join, Right Outer Join, Full Outer Join semantics",
            "Tuple Relational Calculus (TRC) vs Domain Relational Calculus (DRC)",
            "Query optimization: Heuristic query execution trees, pushing selections down"
        ],
        "key_takeaways": "The Division operator (A / B) solves 'all' queries (e.g., find students enrolled in ALL courses taught by Professor X). Pushing selections down reduces Cartesian product sizes early."
    },
    {
        "chapter_num": 3,
        "title": "Functional Dependencies, Normalization & Decomposition (1NF to BCNF)",
        "topics": [
            "Functional Dependencies (FDs) definition and Armstrong's Axioms (Reflexivity, Augmentation, Transitivity)",
            "Attribute Closure (X+) algorithm and Candidate Key determination",
            "Minimal / Canonical Cover computation algorithm",
            "Normal Forms: 1NF (atomic values), 2NF (no partial dependency), 3NF (no transitive dependency), BCNF (strictly superkey LHS)",
            "Decomposition properties: Lossless Join test (R1 intersection R2 -> R1 or R2) and Dependency Preservation test"
        ],
        "key_takeaways": "A relation is in BCNF if for every non-trivial FD X -> Y, X is a superkey. BCNF decomposition guarantees lossless join, but does not always preserve functional dependencies; 3NF guarantees both."
    },
    {
        "chapter_num": 4,
        "title": "Transaction Management, ACID Properties & Concurrency Control",
        "topics": [
            "ACID properties: Atomicity (WAL), Consistency, Isolation (Locks), Durability",
            "Transaction states: Active, Partially Committed, Failed, Aborted, Committed",
            "Schedules & Serializability: Conflict Serializability vs View Serializability",
            "Precedence Graph (Serialization Graph) topological sorting for cycle detection",
            "Concurrency anomalies: Dirty Read (read uncommitted), Non-repeatable Read, Phantom Read, Lost Update",
            "Concurrency control protocols: Two-Phase Locking (2PL, Strict 2PL, Rigorous 2PL), Timestamp Ordering"
        ],
        "key_takeaways": "A schedule is conflict serializable if its precedence graph contains no directed cycles. Strict 2PL prevents cascading rollbacks by holding exclusive write locks until the transaction commits."
    },
    {
        "chapter_num": 5,
        "title": "Crash Recovery & Storage Architecture: WAL & ARIES",
        "topics": [
            "Failure classification: Transaction failure, System crash, Disk failure",
            "Buffer management policies: Steal / No-Steal and Force / No-Force",
            "Write-Ahead Logging (WAL) protocol: Log record must reach non-volatile disk before database page",
            "Checkpointing mechanics: Checkpoint records and active transaction tables",
            "ARIES recovery algorithm: Analysis phase, Redo phase (repeating history), Undo phase (rolling back losers)"
        ],
        "key_takeaways": "Modern enterprise DBMS use Steal/No-Force buffer management for maximum throughput, necessitating both Redo and Undo operations during crash recovery governed by the WAL protocol."
    },
    {
        "chapter_num": 6,
        "title": "Database Storage, File Organization & B+ Tree Indexing",
        "topics": [
            "Storage hierarchy: Memory vs Flash SSD vs Magnetic HDD block access",
            "File organization: Heap files, Sorted files, Hashing (Static vs Dynamic Extendible Hashing)",
            "Indexing architectures: Clustered vs Non-clustered, Primary vs Secondary, Dense vs Sparse indices",
            "B-Trees vs B+ Trees structural comparison (data pointers exclusively in leaf nodes in B+ Trees)",
            "B+ Tree operations: Search O(log_B N), node splitting on overflow, node merging on underflow"
        ],
        "key_takeaways": "B+ Trees store all actual record pointers in leaf nodes linked as a doubly-linked list, providing both O(log N) point queries and lightning-fast sequential range scans."
    },
    {
        "chapter_num": 7,
        "title": "Solved DBMS Placement Problems & Interview Assessment Drills",
        "topics": [
            "Candidate key computation step-by-step proofs",
            "Normal form classification & BCNF lossless decomposition",
            "Precedence graph cycle tracing for conflict serializability",
            "B+ Tree fanout, height, and maximum record capacity calculations",
            "SQL vs Relational Algebra translation puzzles"
        ],
        "key_takeaways": "Mastering Armstrong closure, serializability precedence graphs, and B+ tree node order equations guarantees top-percentile placement technical test performance."
    }
]

DBMS_TEXTBOOK_MARKDOWN = r"""# Database Management Systems: Complete Master Edition (Prescribed Textbook)

**Edition:** 2026 Campus Placement Edition  
**Subject:** Database Management Systems (DBMS)  
**Courseware Board:** Prescribed Placement Architectural Board  
**Status:** In-App Complete Master Textbook (Full Curriculum Available In-Platform)

> **🔒 EXAM GROUNDING POLICY:** All campus placement assessments, DBMS technical interviews, and online test questions are strictly grounded in the relational algebra, normalization theorems, concurrency protocols, and indexing mathematics detailed in this textbook.

---

## 📑 Complete Table of Contents

- [Chapter 1: DBMS Architecture, Relational Model & ER Modeling](#chapter-1-dbms-architecture-relational-model--er-modeling)
  - [1.1 3-Schema Architecture & Data Independence](#11-3-schema-architecture--data-independence)
  - [1.2 Entity-Relationship (ER) Modeling Principles](#12-entity-relationship-er-modeling-principles)
  - [1.3 Mapping ER Diagrams to Relational Schemas](#13-mapping-er-diagrams-to-relational-schemas)
  - [1.4 Relational Integrity Constraints](#14-relational-integrity-constraints)
- [Chapter 2: Relational Algebra, Tuple Calculus & Query Processing](#chapter-2-relational-algebra-tuple-calculus--query-processing)
  - [2.1 Fundamental & Derived Relational Algebra Operators](#21-fundamental--derived-relational-algebra-operators)
  - [2.2 The Relational Division Operator for Universal Quantification](#22-the-relational-division-operator-for-universal-quantification)
  - [2.3 Query Trees & Heuristic Optimization](#23-query-trees--heuristic-optimization)
- [Chapter 3: Functional Dependencies, Normalization & Decomposition (1NF to BCNF)](#chapter-3-functional-dependencies-normalization--decomposition-1nf-to-bcnf)
  - [3.1 Functional Dependencies & Armstrong's Axioms](#31-functional-dependencies--armstrongs-axioms)
  - [3.2 Candidate Key Determination via Attribute Closure](#32-candidate-key-determination-via-attribute-closure)
  - [3.3 Normal Forms Hierarchy: 1NF, 2NF, 3NF & BCNF](#33-normal-forms-hierarchy-1nf-2nf-3nf--bcnf)
  - [3.4 Lossless Join & Dependency Preservation Proofs](#34-lossless-join--dependency-preservation-proofs)
- [Chapter 4: Transaction Management, ACID Properties & Concurrency Control](#chapter-4-transaction-management-acid-properties--concurrency-control)
  - [4.1 ACID Properties Deep Dive](#41-acid-properties-deep-dive)
  - [4.2 Concurrency Anomalies & SQL Isolation Levels](#42-concurrency-anomalies--sql-isolation-levels)
  - [4.3 Conflict Serializability & Precedence Graphs](#43-conflict-serializability--precedence-graphs)
  - [4.4 Locking Protocols: 2PL, Strict 2PL & Rigorous 2PL](#44-locking-protocols-2pl-strict-2pl--rigorous-2pl)
- [Chapter 5: Crash Recovery & Storage Architecture: WAL & ARIES](#chapter-5-crash-recovery--storage-architecture-wal--aries)
  - [5.1 Buffer Management: Steal/No-Steal and Force/No-Force](#51-buffer-management-stealno-steal-and-forceno-force)
  - [5.2 Write-Ahead Logging (WAL) Protocol](#52-write-ahead-logging-wal-protocol)
  - [5.3 The ARIES Recovery Algorithm (Analysis, Redo, Undo)](#53-the-aries-recovery-algorithm-analysis-redo-undo)
- [Chapter 6: Database Storage, File Organization & B+ Tree Indexing](#chapter-6-database-storage-file-organization--b-tree-indexing)
  - [6.1 Clustered vs Non-Clustered Indices](#61-clustered-vs-non-clustered-indices)
  - [6.2 B-Trees vs B+ Trees Architecture](#62-b-trees-vs-b-trees-architecture)
  - [6.3 B+ Tree Node Capacity, Height & Search Complexity](#63-b-tree-node-capacity-height--search-complexity)
- [Chapter 7: Solved DBMS Placement Problems & Interview Assessment Drills](#chapter-7-solved-dbms-placement-problems--interview-assessment-drills)
  - [Solved Problem 1: Candidate Key & BCNF Decomposition Proof](#solved-problem-1-candidate-key--bcnf-decomposition-proof)
  - [Solved Problem 2: Precedence Graph Serializability Analysis](#solved-problem-2-precedence-graph-serializability-analysis)
  - [Solved Problem 3: B+ Tree Fanout & Maximum Records Numerical](#solved-problem-3-b-tree-fanout--maximum-records-numerical)
  - [Self-Assessment Practice Exercises & Verified Solutions](#self-assessment-practice-exercises--verified-solutions)

---

## Chapter 1: DBMS Architecture, Relational Model & ER Modeling

### 1.1 3-Schema Architecture & Data Independence
The ANSI/SPARC 3-Schema Architecture separates user views from internal physical storage:

```
[ External Level ]  -> View 1 (Student View)  View 2 (Faculty View)  View 3 (Finance View)
      |
      |   (Logical Data Independence)
      v
[ Conceptual Level ] -> Global Relational Schema (Tables, Foreign Keys, Constraints)
      |
      |   (Physical Data Independence)
      v
[ Internal Level ]   -> Storage structures (B+ trees, page layouts, hashing, file paths)
```

1. **Logical Data Independence:** The capacity to modify the conceptual schema (adding columns, splitting tables) without having to alter existing external schemas or rewrite user application queries.
2. **Physical Data Independence:** The capacity to alter internal storage structures (adding B+ tree indexes, migrating from HDD to SSD, changing block sizes) without requiring changes to the conceptual or external schema.

### 1.2 Entity-Relationship (ER) Modeling Principles
- **Entity:** An identifiable real-world object (e.g., `Student`, `Course`).
- **Weak Entity:** An entity that cannot be uniquely identified by its own attributes alone and possesses no primary key. It depends on an **Identifying Owner Entity** via an **Identifying Relationship**. Its distinguishing attribute is a **Partial Key / Discriminator** (denoted with a dashed underline in Chen notation).
- **Cardinality Ratios:** $1:1$ (One-to-One), $1:N$ (One-to-Many), $M:N$ (Many-to-Many).
- **Participation Constraints:**
  - **Total Participation (Double Line):** Every entity instance must participate in the relationship (e.g., every `Employee` MUST belong to a `Department`).
  - **Partial Participation (Single Line):** Some entity instances may not participate.

### 1.3 Mapping ER Diagrams to Relational Schemas
1. **Strong Entity Set:** Map directly to a table with all simple attributes. Choose candidate key as Primary Key.
2. **Weak Entity Set:** Create table containing all simple attributes of weak entity + Primary Key of Identifying Owner Entity as Foreign Key. Composite Primary Key = (Owner PK + Partial Discriminator).
3. **1:N Relationship:** Place the Primary Key of the "1" side as a Foreign Key in the table representing the "N" side.
4. **M:N Relationship:** Mandatory creation of a separate **Cross-Reference / Associative Table** containing Foreign Keys referencing both participating entity tables. Primary Key is composite of both foreign keys.
5. **Multivalued Attributes:** Create a new table containing the attribute value + Primary Key of parent entity. Composite PK = (Parent PK + Attribute Value).

### 1.4 Relational Integrity Constraints
- **Domain Constraint:** Values in a column must strictly adhere to the declared data type and nullability definition.
- **Entity Integrity Constraint:** No primary key column value may be `NULL`.
- **Referential Integrity Constraint:** A Foreign Key value in table $R_1$ referencing table $R_2$ must either match an existing Primary Key value in $R_2$ or be `NULL`.
  - Cascading Actions: `ON DELETE CASCADE` (deletes dependent child rows), `ON DELETE SET NULL` (nullifies foreign key column), `ON DELETE RESTRICT / NO ACTION` (rejects parent deletion if child references exist).

---

## Chapter 2: Relational Algebra, Tuple Calculus & Query Processing

### 2.1 Fundamental & Derived Relational Algebra Operators
Relational algebra is a procedural query language consisting of operations that take one or two relations as input and produce a new relation as output:

1. **Selection ($\sigma_C(R)$):** Filters rows satisfying predicate $C$. Unary, commutative: $\sigma_{C_1}(\sigma_{C_2}(R)) = \sigma_{C_2}(\sigma_{C_1}(R))$.
2. **Projection ($\pi_{A_1, \dots, A_k}(R)$):** Selects specified columns and removes duplicate rows (relational sets).
3. **Cartesian Product ($R \times S$):** Combines every tuple of $R$ ($n_1$ rows, $m_1$ cols) with every tuple of $S$ ($n_2$ rows, $m_2$ cols), producing $n_1 \times n_2$ rows and $m_1 + m_2$ columns.
4. **Set Union ($R \cup S$), Intersection ($R \cap S$), Difference ($R - S$):** Require relations to be **Union Compatible** (identical number of attributes with corresponding compatible domains).
5. **Natural Join ($R \bowtie S$):** Performs equality match on all common attribute names and projects out duplicate columns:
   $$R \bowtie S = \pi_{\text{Distinct Attrs}}(\sigma_{R.A = S.A}(R \times S))$$
6. **Theta Join ($R \bowtie_\theta S$):** Cartesian product followed by selection condition $\theta$: $\sigma_\theta(R \times S)$.

### 2.2 The Relational Division Operator for Universal Quantification
The division operator ($R \div S$) is used for queries involving the phrase **"for all"** or **"every"**:
- Let $R$ have attributes $(A, B)$ and $S$ have attribute $(B)$.
- $R \div S$ returns all values of $A$ from $R$ that are associated with **every** value of $B$ in $S$.

$$\text{Definition: } R \div S = \pi_A(R) - \pi_A((\pi_A(R) \times S) - R)$$

*Interview Example:* Find students who have taken all courses offered in the Computer Science department:
$$\pi_{\text{StudentID, CourseID}}(\text{Takes}) \div \pi_{\text{CourseID}}(\sigma_{\text{Dept} = 'CS'}(\text{Courses}))$$

---

## Chapter 3: Functional Dependencies, Normalization & Decomposition (1NF to BCNF)

### 3.1 Functional Dependencies & Armstrong's Axioms
A functional dependency $X \to Y$ holds on relation $R$ if for every pair of tuples $t_1, t_2 \in R$, whenever $t_1[X] = t_2[X]$, then $t_1[Y] = t_2[Y]$.

**Armstrong's Axioms (Sound and Complete):**
1. **Reflexivity Rule:** If $Y \subseteq X$, then $X \to Y$. (Trivial dependency)
2. **Augmentation Rule:** If $X \to Y$, then $XZ \to YZ$ for any attribute set $Z$.
3. **Transitivity Rule:** If $X \to Y$ and $Y \to Z$, then $X \to Z$.

**Derived Secondary Rules:**
- **Union:** If $X \to Y$ and $X \to Z$, then $X \to YZ$.
- **Decomposition:** If $X \to YZ$, then $X \to Y$ and $X \to Z$.
- **Pseudo-Transitivity:** If $X \to Y$ and $WY \to Z$, then $WX \to Z$.

### 3.2 Candidate Key Determination via Attribute Closure
**Attribute Closure ($X^+$):** The complete set of all attributes functionally determined by $X$ under a set of FDs $F$.

**Algorithm to Compute $X^+$:**
1. Initialize $\text{closure} = X$.
2. Repeat until no more attributes can be added:
   - For each FD $Y \to Z \in F$:
     - If $Y \subseteq \text{closure}$, then $\text{closure} = \text{closure} \cup Z$.
3. Return $\text{closure}$.

**Candidate Key Test:** $X$ is a **Candidate Key** of relation $R$ if:
1. $X^+ = R$ (Superkey property: determines all attributes in the relation).
2. For no proper subset $Y \subset X$ does $Y^+ = R$ (Minimality property).

### 3.3 Normal Forms Hierarchy: 1NF, 2NF, 3NF & BCNF

```
+---------------------------------------------------------------+
| BCNF: For every non-trivial X -> Y, X must be a Superkey       |
|   +-------------------------------------------------------+   |
|   | 3NF: For every X -> Y, X is Superkey OR Y is Prime    |   |
|   |   +-----------------------------------------------+   |   |
|   |   | 2NF: No non-prime attribute partially depends |   |   |
|   |   |      on any candidate key                     |   |   |
|   |   |   +---------------------------------------+   |   |   |
|   |   |   | 1NF: All attribute values are atomic   |   |   |   |
|   |   |   +---------------------------------------+   |   |   |
|   |   +-----------------------------------------------+   |   |
|   +-------------------------------------------------------+   |
+---------------------------------------------------------------+
```

- **First Normal Form (1NF):** Every column contains strictly atomic (indivisible) values. No repeating groups or nested arrays.
- **Second Normal Form (2NF):** Must be in 1NF, and **NO non-prime attribute is partially dependent on any candidate key**. (A partial dependency occurs when a proper subset of a composite candidate key determines a non-prime attribute).
- **Third Normal Form (3NF):** Must be in 2NF, and for every non-trivial functional dependency $X \to Y$:
  - Either $X$ is a **Superkey**, OR
  - $Y$ is a **Prime Attribute** (a member of any candidate key).
  *(Eliminates transitive dependencies between non-prime attributes).*
- **Boyce-Codd Normal Form (BCNF):** Must be in 3NF, and for every non-trivial functional dependency $X \to Y$:
  - **$X$ MUST be a Superkey.** (No exceptions for prime attributes on the RHS).

### 3.4 Lossless Join & Dependency Preservation Proofs
When decomposing relation $R$ into $R_1$ and $R_2$:

1. **Lossless Join Condition:** The decomposition is lossless if and only if the common attributes form a superkey of at least one of the decomposed relations:
   $$(R_1 \cap R_2) \to R_1 \quad \text{OR} \quad (R_1 \cap R_2) \to R_2$$
2. **Dependency Preservation Condition:** The decomposition preserves dependencies if the union of FDs enforceable on each sub-relation directly recovers the entire original closure: $(F_1 \cup F_2)^+ = F^+$.
   - **Crucial Placement Fact:** Any relation schema can always be decomposed into **3NF** satisfying both **Lossless Join** AND **Dependency Preservation**. Decomposing into **BCNF** guarantees **Lossless Join**, but cannot always preserve functional dependencies.

---

## Chapter 4: Transaction Management, ACID Properties & Concurrency Control

### 4.1 ACID Properties Deep Dive
- **Atomicity:** All-or-nothing execution. Guaranteed by the DBMS recovery manager via Write-Ahead Logging (WAL) and Undo rollback operations.
- **Consistency:** Transactions must transition the database from one valid state satisfying all schema integrity constraints to another valid state.
- **Isolation:** Execution of concurrent transactions produces the same state as if they were executed serially. Controlled by the concurrency control manager (locking, MVCC).
- **Durability:** Once a transaction commits, its updates persist permanently on non-volatile disk storage even in the event of an immediate catastrophic power failure. Guaranteed by Redo logging.

### 4.2 Concurrency Anomalies & SQL Isolation Levels
| SQL Isolation Level | Dirty Read | Non-Repeatable Read | Phantom Read | Mechanism Employed |
|:---|:---:|:---:|:---:|:---|
| **Read Uncommitted** | Possible | Possible | Possible | Transactions read uncommitted dirty buffer pages without locks. |
| **Read Committed** | **Prevented** | Possible | Possible | Short-term Shared read locks released immediately after statement execution; exclusive locks held until commit. (PostgreSQL / Oracle default). |
| **Repeatable Read** | **Prevented** | **Prevented** | Possible | Shared read locks held until end of transaction; prevent in-place record updates. (MySQL InnoDB default). |
| **Serializable** | **Prevented** | **Prevented** | **Prevented** | Strict two-phase locking with predicate/range locks or SSI (Serializable Snapshot Isolation). |

### 4.3 Conflict Serializability & Precedence Graphs
Two operations $O_1 \in T_1$ and $O_2 \in T_2$ are in **conflict** if:
1. They belong to different transactions ($T_1 \ne T_2$).
2. They operate on the same data item $Q$.
3. At least one of the operations is a **Write** ($W(Q)$).
*(Conflicts: Read-Write, Write-Read, Write-Write).*

**Precedence Graph (Serialization Graph) Algorithm:**
1. Create a node for each committed transaction $T_i$.
2. Draw a directed edge $T_i \to T_j$ if an operation in $T_i$ conflicts with an operation in $T_j$, and $T_i$ executed the operation before $T_j$.
3. **Serializability Theorem:** A schedule $S$ is **Conflict Serializable** if and only if its precedence graph contains **NO directed cycles**.
4. The equivalent serial schedule order is obtained by performing a **Topological Sort** on the acyclic graph.

### 4.4 Locking Protocols: 2PL, Strict 2PL & Rigorous 2PL
- **Two-Phase Locking (2PL):**
  - **Growing Phase:** Transaction may acquire locks, but cannot release any lock.
  - **Lock Point:** Moment when the transaction has acquired all necessary locks.
  - **Shrinking Phase:** Transaction may release locks, but cannot acquire any new lock.
  - *Guarantees Conflict Serializability, but susceptible to Cascading Rollbacks and Deadlocks.*
- **Strict 2PL:** All **Exclusive (Write) locks** acquired by a transaction must be held until the transaction explicitly Commits or Aborts. *(Prevents Cascading Aborts).*
- **Rigorous 2PL:** All **Exclusive (Write) and Shared (Read) locks** must be held until transaction termination. *(Guarantees Strictness and easy recovery).*

---

## Chapter 5: Crash Recovery & Storage Architecture: WAL & ARIES

### 5.1 Buffer Management: Steal/No-Steal and Force/No-Force
- **Steal Policy:** The buffer manager can flush dirty pages modified by an active uncommitted transaction to disk to free RAM frames. *(Requires Undo logging to rollback on crash).*
- **No-Force Policy:** The buffer manager does not force dirty committed pages to disk at commit time. *(Requires Redo logging to reapply committed writes on crash).*
- **Industry Standard:** Enterprise DBMS (PostgreSQL, MySQL, Oracle) utilize **Steal / No-Force** because it maximizes disk I/O throughput by avoiding synchronous random disk writes at transaction commit.

### 5.2 Write-Ahead Logging (WAL) Protocol
The WAL protocol mandates two fundamental rules before writing data to disk:
1. **Rule 1 (Undo Rule):** Before a dirty database frame is written from memory to disk (Steal), the log records associated with the update must be flushed to stable disk storage.
2. **Rule 2 (Redo Rule):** Before a transaction is acknowledged as committed (No-Force), all of its log records (including the `COMMIT` record) must be flushed to stable disk storage.

### 5.3 The ARIES Recovery Algorithm (Analysis, Redo, Undo)
Developed by C. Mohan at IBM, ARIES recovers from crashes in 3 distinct sequential passes over the transaction log:

1. **Analysis Pass:** Scans forward from the last checkpoint to the end of the log:
   - Reconstructs the **Dirty Page Table (DPT)** and the active **Transaction Table (TT)**.
   - Identifies all "Loser" transactions that were active when the system crashed.
2. **Redo Pass (Repeating History):** Scans forward from the smallest `RecLSN` in the DPT to the end of the log:
   - Re-executes the actions of ALL transactions (both committed and uncommitted) to restore the database buffer pool to the exact state at the instant of crash.
3. **Undo Pass:** Scans backward from the end of the log:
   - Rolls back the operations of all "Loser" transactions in reverse chronological order.
   - Writes **Compensation Log Records (CLRs)** for each undone operation to prevent cascading undo in case of crashes during the recovery process itself.

---

## Chapter 6: Database Storage, File Organization & B+ Tree Indexing

### 6.1 Clustered vs Non-Clustered Indices
| Architectural Metric | Clustered Index (Primary Index) | Non-Clustered Index (Secondary Index) |
|:---|:---|:---|
| **Data Row Organization** | The physical order of data rows on disk strictly matches the index key order. | The physical order of data rows on disk is independent of index order. |
| **Indices Allowed Per Table** | Strictly **1** clustered index per table (since data can only be physically sorted one way). | Multiple secondary indexes allowed per table (typically up to 64 or 128). |
| **Leaf Node Content** | Leaf nodes ARE the actual data records (or data pages containing full rows). | Leaf nodes store the index key value + a pointer (RID or Primary Key) to the row. |
| **Range Scan Performance** | Ultra-fast sequential I/O; rows on adjacent pages are contiguous on disk. | Slower; requires random disk lookups for each pointer unless covering index is used. |

### 6.2 B-Trees vs B+ Trees Architecture
- **B-Tree:** Data pointers (pointers to actual table rows) are stored in internal nodes as well as leaf nodes.
  - *Drawback:* Internal nodes have low fan-out because large data pointers occupy node space, leading to deeper trees and higher disk I/O.
- **B+ Tree:**
  - **Internal Nodes:** Store strictly search keys and child node page pointers. High fan-out ($B \approx 100 \text{ to } 500$), resulting in shallow tree heights of only 3 or 4 levels.
  - **Leaf Nodes:** Store all actual data records (or RIDs) along with search keys.
  - **Linked Leaves:** Leaf nodes are chained together in a **Doubly-Linked List**, enabling blazing-fast $O(k)$ range scan queries (`WHERE salary BETWEEN 50000 AND 80000`).

### 6.3 B+ Tree Node Capacity, Height & Search Complexity
Let $B$ be the order (fan-out) of a B+ tree node, $P$ be disk block size, $K$ be key size, and $p_t$ be pointer size:
$$B \times p_t + (B - 1) \times K \le P \implies B \le \frac{P + K}{p_t + K}$$

- **Search Time Complexity:** Point query takes $O(\log_B N)$ disk block reads.
- **Tree Height:** $h \le \lceil \log_{\lceil B / 2 \rceil} (N) \rceil + 1$. For a fanout $B = 200$, a 3-level B+ tree can index:
  $$N \approx 200^3 = 8,000,000 \text{ records with at most 3 disk I/O operations!}$$

---

## Chapter 7: Solved DBMS Placement Problems & Interview Assessment Drills

### Solved Problem 1: Candidate Key & BCNF Decomposition Proof
- **Problem:** Relation $R(A, B, C, D, E)$ with functional dependencies:
  $$F = \{ A \to BC, \ CD \to E, \ B \to D, \ E \to A \}$$
  1. Find all candidate keys of $R$.
  2. Determine the highest normal form of $R$.
  3. If not in BCNF, decompose $R$ into BCNF relations losslessly.
- **Solution:**
  1. **Candidate Key Determination:**
     - Check attribute occurrences: $A$ is on LHS, $B$ on RHS, $C$ on RHS, $D$ on RHS, $E$ on RHS. Neither $C$ nor $D$ appears alone on LHS.
     - Compute $A^+$:
       - Start with $\{A\}$.
       - $A \to BC \implies \{A, B, C\}$.
       - $B \to D \implies \{A, B, C, D\}$.
       - $CD \to E \implies \{A, B, C, D, E\} = R$.
       - Hence, **$A$ is a candidate key**.
     - Since $E \to A$, compute $E^+$:
       - $\{E\} \to \{E, A\} \to \{E, A, B, C, D\} = R$.
       - Hence, **$E$ is a candidate key**.
     - Check if $CD$ or $BC$ can derive $A$:
       - $(CD)^+ = \{C, D, E, A, B\} = R$. But does a subset work? $C^+ = \{C\}$, $D^+ = \{D\}$. So **$CD$ is a candidate key**.
       - Since $B \to D$, $(BC)^+ = (BCD)^+ = \{B, C, D, E, A\} = R$. Can a subset work? $B^+ = \{B, D\}$, $C^+ = \{C\}$. Neither is a superkey. So **$BC$ is a candidate key**.
     - Candidate Keys: **$\{A\}, \{E\}, \{CD\}, \{BC\}$**.
     - Prime Attributes: $\{A, B, C, D, E\}$ (All attributes are prime!).
  2. **Highest Normal Form:**
     - Is it in 1NF? Yes (atomic attributes).
     - Is it in 2NF? Check for partial dependencies:
       - $CD$ is a candidate key. $D$ is non-prime? No, all attributes are prime. In 2NF, partial dependency is defined strictly as a proper subset of a key determining a *non-prime* attribute. Since all attributes are prime, no non-prime attribute exists $\implies$ **2NF holds**.
     - Is it in 3NF?
       - For $X \to Y$, either $X$ is superkey or $Y$ is prime.
       - Since every attribute is prime, the condition "$Y$ is prime" holds vacuously for all FDs in $F$!
       - Therefore, $R$ is in **3NF**.
     - Is it in BCNF?
       - Check FD $B \to D$: Is $B$ a superkey? $B^+ = \{B, D\} \ne R$. $B$ is NOT a superkey.
       - Therefore, $R$ violates BCNF.
       - **Highest Normal Form is 3NF.**
  3. **Lossless BCNF Decomposition:**
     - Decompose along violating FD $B \to D$:
       - $R_1(B, D)$ with FD $\{B \to D\}$. Candidate key is $B$. In BCNF.
       - $R_2(R - \{D\} \cup \{B\}) = R_2(A, B, C, E)$ with FDs $\{A \to BC, E \to A\}$. Candidate keys $\{A\}, \{E\}, \{BC\}$. In BCNF.
     - Lossless check: $R_1 \cap R_2 = \{B\}$. In $R_1$, $B^+ = \{B, D\} = R_1$. Common attribute is a superkey of $R_1 \implies$ **Lossless Join guaranteed**.

### Solved Problem 2: Precedence Graph Serializability Analysis
- **Problem:** Analyze the following schedule $S$ for conflict serializability:
  $$S: R_1(X); \ R_2(X); \ W_1(X); \ R_1(Y); \ W_2(X); \ W_1(Y); \ C_1; \ C_2$$
- **Solution:**
  1. Identify conflicting operations between $T_1$ and $T_2$:
     - $R_2(X)$ occurs before $W_1(X) \implies$ Directed edge: $T_2 \to T_1$.
     - $W_1(X)$ occurs before $W_2(X) \implies$ Directed edge: $T_1 \to T_2$.
  2. Graph Analysis:
     - The precedence graph contains directed edges $T_2 \to T_1$ and $T_1 \to T_2$, forming a directed cycle:
       $$T_1 \rightleftarrows T_2$$
  3. Conclusion: The schedule $S$ is **NOT Conflict Serializable** and will cause race condition inconsistencies.

### Solved Problem 3: B+ Tree Fanout & Maximum Records Numerical
- **Problem:** A database system has disk block size $P = 4096\text{ bytes}$. The search key is $K = 16\text{ bytes}$, and a block pointer is $p = 8\text{ bytes}$.
  1. Calculate the maximum order (fan-out) $B$ of an internal node.
  2. If the leaf nodes have capacity for 30 record entries, calculate the maximum number of records indexed by a 3-level B+ tree (root at level 1, internal nodes at level 2, leaf nodes at level 3).
- **Solution:**
  1. Internal node equation:
     $$B \cdot p + (B - 1) \cdot K \le P$$
     $$B(8) + (B - 1)(16) \le 4096 \implies 8B + 16B - 16 \le 4096 \implies 24B \le 4112 \implies B \le 171.33$$
     - Maximum internal node order (fan-out) is $\mathbf{B = 171}$.
  2. Capacity for 3-level B+ tree:
     - Level 1 (Root): 1 node with up to $B = 171$ child pointers.
     - Level 2 (Internal): Up to 171 nodes, each having up to 171 leaf pointers $\implies 171 \times 171 = 29,241$ leaf nodes.
     - Level 3 (Leaf): Each leaf node stores 30 records.
     - Maximum Records $= 29,241 \times 30 = \mathbf{877,230\text{ records}}$.

---

### Self-Assessment Practice Exercises & Verified Solutions:

1. **Exercise 1 (Relational Algebra):** Given relations $\text{Employee}(\text{EmpId}, \text{Name}, \text{DeptId})$ and $\text{Department}(\text{DeptId}, \text{DeptName})$, write a relational algebra expression to retrieve the names of employees working in the 'Research' department.
   - *Solution:* $\pi_{\text{Name}}(\sigma_{\text{DeptName} = 'Research'}(\text{Employee} \bowtie \text{Department}))$.

2. **Exercise 2 (Decomposition Test):** Relation $R(A, B, C)$ with $FD = \{A \to B\}$ is decomposed into $R_1(A, B)$ and $R_2(B, C)$. Is the decomposition lossless?
   - *Solution:* $R_1 \cap R_2 = \{B\}$. For lossless join, $B$ must determine $R_1$ ($B \to A$) or $R_2$ ($B \to C$). Since $B^+ = \{B\}$, $B$ is neither a superkey of $R_1$ nor $R_2$. Therefore, the decomposition is **Lossy**.

3. **Exercise 3 (Strict 2PL vs 2PL):** Why does Strict 2PL prevent cascading rollbacks while basic 2PL does not?
   - *Solution:* In basic 2PL, a transaction can release an exclusive write lock in its shrinking phase before committing. Another transaction can read that updated uncommitted data. If the first transaction subsequently aborts, the second transaction must also be rolled back (cascading abort). In Strict 2PL, all exclusive locks are retained until commit/abort, guaranteeing that uncommitted data is never exposed.

4. **Exercise 4 (ARIES CLR Log Records):** What is the purpose of Compensation Log Records (CLRs) written during the Undo phase of the ARIES recovery algorithm?
   - *Solution:* CLRs record the reversal of an aborted transaction's update. Each CLR contains an `UndoNextLSN` pointer pointing to the next log record to be undone. If the system crashes during the recovery undo phase itself, ARIES uses the CLR and `UndoNextLSN` to resume undo without repeating already undone operations, preventing infinite recovery loops.

5. **Exercise 5 (Cardinality of Cross Product):** Relation $R$ has 1,000 tuples and relation $S$ has 2,000 tuples. What are the minimum and maximum possible number of tuples in $R \bowtie S$ (natural join on common attribute $A$)?
   - *Solution:* Minimum tuples $= 0$ (if no values of $A$ match between $R$ and $S$). Maximum tuples $= 1,000 \times 2,000 = \mathbf{2,000,000}$ (if all tuples in both relations have the exact same value for attribute $A$).
"""

DBMS_EXPANDED_QUESTIONS = [
    {
        "chapter_num": 3,
        "chapter_title": "Functional Dependencies, Normalization & Decomposition (1NF to BCNF)",
        "subtopic": "BCNF Definition",
        "question": "Which condition must hold for every non-trivial functional dependency X -> Y in a relational schema to be strictly in Boyce-Codd Normal Form (BCNF)?",
        "options": [
            "X must be a Superkey",
            "Y must be a Prime Attribute",
            "X must be a proper subset of a candidate key",
            "Y must contain no composite domains"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [DBMS Prescribed Textbook — Chapter 3: Normalization]\nA relation is in BCNF if for every non-trivial FD X -> Y, the left-hand side X is strictly a Superkey. 3NF allows Y to be a prime attribute, but BCNF removes that exception.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 4,
        "chapter_title": "Transaction Management, ACID Properties & Concurrency Control",
        "subtopic": "Conflict Serializability",
        "question": "Under the Precedence Graph (Serialization Graph) testing method, when is a concurrent schedule guaranteed to be conflict serializable?",
        "options": [
            "If and only if the precedence graph contains no directed cycles",
            "If all transactions execute 2-phase commit",
            "If all read operations precede write operations",
            "If the total number of transactions is fewer than the available CPU cores"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [DBMS Prescribed Textbook — Chapter 4: Concurrency Control]\nA schedule is conflict serializable if and only if its precedence graph contains no directed cycles. An acyclic precedence graph allows topological sorting to find an equivalent serial order.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 6,
        "chapter_title": "Database Storage, File Organization & B+ Tree Indexing",
        "subtopic": "B+ Tree Leaf Node Structure",
        "question": "Why do B+ Trees provide superior performance for SQL range scan queries compared to standard B-Trees?",
        "options": [
            "All leaf nodes in a B+ Tree are linked together in a doubly-linked list, allowing sequential traversal without traversing the tree root repeatedly",
            "B+ Trees store data records only in the root node",
            "B+ Trees use hash buckets instead of sorted pointers",
            "B+ Trees eliminate all disk block read operations"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [DBMS Prescribed Textbook — Chapter 6: B+ Tree Indexing]\nIn a B+ Tree, leaf nodes contain all keys and data pointers and are linked in a continuous doubly-linked list. A range query (e.g. BETWEEN A AND B) locates the starting leaf in O(log N) and then traverses sequentially through the leaf list.",
        "difficulty": "easy",
    }
]
'''

with open(os.path.join(TEXTBOOK_DIR, "cn_master.py"), "w", encoding="utf-8") as f:
    f.write(CN_CODE.strip() + "\n")
ast.parse(CN_CODE)
print("cn_master.py generated and syntax verified!")

with open(os.path.join(TEXTBOOK_DIR, "dbms_master.py"), "w", encoding="utf-8") as f:
    f.write(DBMS_CODE.strip() + "\n")
ast.parse(DBMS_CODE)
print("dbms_master.py generated and syntax verified!")

