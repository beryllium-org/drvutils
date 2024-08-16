rename_process("drv2605vib")
vr("opts", be.api.xarg())
be.api.setvar("return", "1")
if "i" in vr("opts")["o"]:
    vr("busn", 0)
    if vr("opts")["o"]["i"] is not None:
        try:
            vr("nbus", vr("opts")["o"]["i"])
            if not vr("nbus").startswith("/dev/i2c"):
                raise RuntimeError
            vr("busn", int(vr("opts")["o"]["i"][-1:]))
        except:
            term.write("Could not parse node, using default.")
    try:
        vr("i2c", be.devices["i2c"][vr("busn")])

        class vibrator:
            def __init__(self, vibrator, modul):
                self._v = vibrator
                self._e = modul.Effect
                self._p = modul.Pause

            @property
            def sequence(self) -> list:
                return self._v.sequence

            @sequence.setter
            def sequence(self, nseq: list):
                self._v.sequence = nseq

            def play(self) -> None:
                self._v.play()

            def stop(self) -> None:
                self._v.stop()

            def effect(self, value: int):
                if value == -1:
                    return self._p
                else:
                    return self._e(value)

            def pause(self, duration: float):
                return self._p(duration)

        import adafruit_drv2605

        vr("vibn", adafruit_drv2605.DRV2605(vr("i2c")))
        be.based.run("mknod vib")
        vr("node", be.api.getvar("return"))
        be.api.subscript("/bin/stringproccessing/devid.py")
        be.devices["vib"][vr("dev_id")] = vibrator(vr("vibn"), adafruit_drv2605)
        del vibrator, adafruit_drv2605
        dmtex("Created DRV2605 vibration device")
    except:
        dmtex("Failed to load DRV2605 vibration motor!")
        try:
            del vibrator, adafruit_drv2605
        except NameError:
            pass
    be.api.setvar("return", "0")
elif "d" in vr("opts")["o"]:
    vr("dev", vr("opts")["o"]["d"])
    if vr("dev") is not None and vr("dev").startswith("/dev/vib"):
        be.based.run("rmnod " + vr("dev")[5:])
        be.api.setvar("return", "0")
    else:
        term.write("Invalid device node!")
else:
    term.write(
        "Usage:\n drv2605vib    -i\n    drv2605vib -i /dev/i2cX\n    drv2605vib -d"
    )
