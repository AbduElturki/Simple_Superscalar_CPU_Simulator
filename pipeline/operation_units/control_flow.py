from .op_unit import op_unit

class control_flow(op_unit):
    def execute(self, cpu):
        decode = self.decode
        if decode[1] in range(0x4):
            cpu.instruct_per_cycle[cpu.cycle] += 1
            self.clear()

        elif decode[1] >= 0x4:
            r1 = cpu.get_value(decode[2])
            r2 = decode[3]
            forward = cpu.is_spec_forward()
            if decode[1] is 0x4:
                if r1 >= 0:
                    if cpu.speculate_mode() is "target":
                        cpu.spec_merge()
                        cpu.update_branch_pred(True, forwad)
                        cpu.commit_fork("target")
                    else:
                        cpu.spec_flush()
                        cpu.update_branch_pred(False, forwad)
                        cpu.commit_fork("sequential")
                else:
                    if cpu.speculate_mode() is "sequential":
                        cpu.spec_merge()
                        cpu.update_branch_pred(False, forwad)
                        cpu.commit_fork("sequential")
                    else:
                        cpu.spec_flush()
                        cpu.update_branch_pred(True, forwad)
                        cpu.commit_fork("target")
                self.clear()
            elif decode[1] is 0x5:
                if r1 < 0:
                    if cpu.speculate_mode() is "target":
                        cpu.spec_merge()
                        cpu.update_branch_pred(True, forwad)
                        cpu.commit_fork("target")
                    else:
                        cpu.spec_flush()
                        cpu.update_branch_pred(False, forwad)
                        cpu.commit_fork("sequential")
                else:
                    if cpu.speculate_mode() is "sequential":
                        cpu.spec_merge()
                        cpu.update_branch_pred(False, forwad)
                        cpu.commit_fork("sequential")
                    else:
                        cpu.spec_flush()
                        cpu.update_branch_pred(True, forwad)
                        cpu.commit_fork("target")
                self.clear()
            elif decode[1] is 0x6:
                if r1 != 0:
                    if cpu.speculate_mode() is "target":
                        cpu.spec_merge()
                        cpu.update_branch_pred(True, forwad)
                        cpu.commit_fork("target")
                    else:
                        cpu.spec_flush()
                        cpu.update_branch_pred(False, forwad)
                        cpu.commit_fork("sequential")
                else:
                    if cpu.speculate_mode() is "sequential":
                        cpu.spec_merge()
                        cpu.update_branch_pred(False, forwad)
                        cpu.commit_fork("sequential")
                    else:
                        cpu.spec_flush()
                        cpu.update_branch_pred(True, forwad)
                        cpu.commit_fork("target")
                self.clear()
            elif decode[1] is 0x7:
                if r1 > 0:
                    if cpu.speculate_mode() is "target":
                        cpu.spec_merge()
                        cpu.update_branch_pred(True, forwad)
                        cpu.commit_fork("target")
                    else:
                        cpu.spec_flush()
                        cpu.update_branch_pred(False, forwad)
                        cpu.commit_fork("sequential")
                else:
                    if cpu.speculate_mode() is "sequential":
                        cpu.spec_merge()
                        cpu.update_branch_pred(False, forwad)
                        cpu.commit_fork("sequential")
                    else:
                        cpu.spec_flush()
                        cpu.update_branch_pred(True, forwad)
                        cpu.commit_fork("target")
                self.clear()
            else:
                raise Exception("In conditional branch section of control_flow\
                                , decode[1] is larger than 0x7")
            cpu.instruct_per_cycle[cpu.cycle] += 1
