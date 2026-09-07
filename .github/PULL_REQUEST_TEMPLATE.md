### 🛡️ Open-Sentinel Change Control & Verification

#### Summary
<!-- Brief description of the architectural change, fix, or capability introduced -->

#### Checklist
- [ ] Code compiles cleanly without bytecode warnings (`python -m py_compile`).
- [ ] Bandit SAST vulnerability scan executed and passed.
- [ ] Zero-Trust secret audit verified (no unmasked keys or webhooks).
- [ ] Documentation updated to reflect changes (`README.md`, `config.example.json`).

#### Classification
- [ ] `type:bug` - Operational defect resolution
- [ ] `type:enhancement` - Capability expansion
- [ ] `type:security` - Security hardening or vulnerability mitigation
- [ ] `type:documentation` - Specification or operational runbooks
