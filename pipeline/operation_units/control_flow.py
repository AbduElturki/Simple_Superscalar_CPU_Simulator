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
            if decode[1] == 0x4:
                if r1 >= 0:
                    cpu.update_branch_pred(True, forward)
                    cpu.commit_fork("target")
                    if cpu.speculate_mode() is "target": #Prediction Correct
                        cpu.correct_branching += 1
                        cpu.spec_merge()
                    else: #Prediction Incorrect
                        cpu.spec_flush()
                else: #Branch not Taken
                    cpu.update_branch_pred(False, forward)
                    cpu.commit_fork("sequential")
                    if cpu.speculate_mode() is "sequential": #Prediction Correct
                        cpu.correct_branching += 1
                        cpu.spec_merge()
                    else: #Prediction Incorrect
                        cpu.spec_flush()
                self.clear()
            elif decode[1] == 0x5:
                if r1 < 0:
                    cpu.update_branch_pred(True, forward)
                    cpu.commit_fork("target")
                    if cpu.speculate_mode() is "target": #Prediction Correct
                        cpu.correct_branching += 1
                        cpu.spec_merge()
                    else: #Prediction Incorrect
                        cpu.spec_flush()
                else: #Branch not Taken
                    cpu.update_branch_pred(False, forward)
                    cpu.commit_fork("sequential")
                    if cpu.speculate_mode() is "sequential": #Prediction Correct
                        cpu.correct_branching += 1
                        cpu.spec_merge()
                    else: #Prediction Incorrect
                        cpu.spec_flush()
                self.clear()
            elif decode[1] == 0x6:
                if r1 == 0: #Branch Taken
                    cpu.update_branch_pred(True, forward)
                    cpu.commit_fork("target")
                    if cpu.speculate_mode() is "target": #Prediction Correct
                        cpu.correct_branching += 1
                        cpu.spec_merge()
                    else: #Prediction Incorrect
                        cpu.spec_flush()
                else: #Branch not Taken
                    cpu.update_branch_pred(False, forward)
                    cpu.commit_fork("sequential")
                    if cpu.speculate_mode() is "sequential": #Prediction Correct
                        cpu.correct_branching += 1
                        cpu.spec_merge()
                    else: #Prediction Incorrect
                        cpu.spec_flush()
                self.clear()
            elif decode[1] == 0x7:
                if r1 > 0:
                    cpu.update_branch_pred(True, forward)
                    cpu.commit_fork("target")
                    if cpu.speculate_mode() is "target": #Prediction Correct
                        cpu.correct_branching += 1
                        cpu.spec_merge()
                    else: #Prediction Incorrect
                        cpu.spec_flush()
                else: #Branch not Taken
                    cpu.update_branch_pred(False, forward)
                    cpu.commit_fork("sequential")
                    if cpu.speculate_mode() is "sequential": #Prediction Correct
                        cpu.correct_branching += 1
                        cpu.spec_merge()
                    else: #Prediction Incorrect
                        cpu.spec_flush()
                self.clear()
            else:
                raise Exception("In conditional branch section ofcontrol_flow," +
                                "decode[1] is larger than 0x7", + decode[1])
            cpu.instruct_per_cycle[cpu.cycle] += 1
